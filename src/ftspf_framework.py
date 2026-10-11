from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover - optional dependency for runtime only
    yf = None

DEFAULT_TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "NFLX",
    "JPM",
    "WMT",
]


def calculate_sentiment_label(daily_return: float, volume_ratio: float) -> str:
    """Rule-based fallback for sentiment when no labelled dataset or model is present.

    This intentionally avoids claiming to be a trained sentiment model. It should be
    treated as a transparent, explainable proxy derived from market movement.
    """
    if daily_return > 0.01 and volume_ratio > 1.0:
        return "Positive"
    if daily_return < -0.01 and volume_ratio < 1.0:
        return "Negative"
    return "Neutral"


def compute_financial_summary(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "total_records": 0,
            "selected_stocks": 0,
            "start_date": None,
            "end_date": None,
            "latest_price": 0.0,
            "latest_prices": {},
            "average_volume": 0.0,
            "average_daily_return": 0.0,
        }

    market_data = df.copy()
    if "Date" in market_data.columns:
        market_data["Date"] = pd.to_datetime(market_data["Date"])
    if "Daily_Return" not in market_data.columns:
        market_data["Daily_Return"] = 0.0
    if "Volume" not in market_data.columns:
        market_data["Volume"] = 0

    ordered = market_data.sort_values("Date").drop_duplicates(subset=["Company", "Date"], keep="last")

    latest_by_company = ordered.sort_values("Date").drop_duplicates("Company", keep="last")
    latest_price = float(latest_by_company["Close"].iloc[-1]) if not latest_by_company.empty else 0.0

    summary = {
        "total_records": int(len(ordered)),
        "selected_stocks": int(ordered["Company"].nunique()),
        "start_date": str(ordered["Date"].min().date()) if "Date" in ordered.columns else None,
        "end_date": str(ordered["Date"].max().date()) if "Date" in ordered.columns else None,
        "latest_price": latest_price,
        "latest_prices": latest_by_company.set_index("Company")["Close"].to_dict(),
        "average_volume": float(ordered["Volume"].mean()) if "Volume" in ordered.columns else 0.0,
        "average_daily_return": float(pd.to_numeric(ordered["Daily_Return"], errors="coerce").mean()),
    }
    return summary


def generate_business_insights(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No market data is available yet for FTSPF analysis."]

    sentiment_counts = df.get("Sentiment_Label", pd.Series(["Neutral"] * len(df))).value_counts()
    avg_return = float(pd.to_numeric(df.get("Daily_Return", 0), errors="coerce").mean())
    positive_share = float((df.get("Sentiment_Label") == "Positive").mean()) if "Sentiment_Label" in df.columns else 0.0

    insights: list[str] = []
    if sentiment_counts.get("Positive", 0) > sentiment_counts.get("Negative", 0):
        insights.append(
            f"Sentiment is positively skewed, with {positive_share:.0%} of observations labelled Positive."
        )
    else:
        insights.append(
            "Sentiment remains mixed, indicating that market confidence is not uniformly positive across the selected stocks."
        )

    if avg_return > 0:
        insights.append(f"Average daily return is positive at {avg_return:.2%}, suggesting mild upward momentum in the selected market window.")
    elif avg_return < 0:
        insights.append(f"Average daily return is negative at {avg_return:.2%}, suggesting weaker performance across the selected market window.")
    else:
        insights.append("Average daily return is near zero, indicating a relatively flat market trend over the selected period.")

    if "Company" in df.columns:
        insights.append(f"The dataset covers {df['Company'].nunique()} companies, giving a diversified but compact FTSPF business-intelligence view.")

    return insights


def fetch_stock_market_data(
    output_dir: str | Path | None = None,
    tickers: list[str] | None = None,
    start_date: str = "2020-01-01",
    end_date: str | None = None,
) -> pd.DataFrame:
    """Fetch stock data using yfinance when available and export a clean CSV for analytics.

    If yfinance is unavailable, this function raises a clear error and directs the user to
    install dependencies via requirements.txt.
    """
    if pathlib_output := output_dir:
        data_dir = Path(pathlib_output)
    else:
        data_dir = Path(__file__).resolve().parents[1] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    if tickers is None:
        tickers = DEFAULT_TICKERS
    if end_date is None:
        end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

    if yf is None:
        raise RuntimeError("yfinance is required to fetch the stock dataset. Install the project dependencies first.")

    frames: list[pd.DataFrame] = []
    for ticker in tickers:
        raw = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
        if raw.empty:
            continue
        df = raw.reset_index()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df["Company"] = ticker
        frames.append(df)

    if not frames:
        raise ValueError("No stock data was available for the selected tickers and date range.")

    market_data = pd.concat(frames, ignore_index=True)
    market_data = market_data.rename(columns={"Adj Close": "Adj_Close"})
    if "Date" not in market_data.columns:
        market_data["Date"] = market_data.index

    preferred_columns = [
        "Date",
        "Company",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj_Close",
        "Volume",
    ]
    for column in preferred_columns:
        if column not in market_data.columns:
            market_data[column] = pd.NA
    market_data = market_data[preferred_columns]

    market_data["Daily_Return"] = market_data.groupby("Company")["Close"].pct_change().fillna(0.0)
    market_data["Volume_Ratio"] = market_data.groupby("Company")["Volume"].transform(
        lambda values: values / values.shift(1).replace(0, pd.NA)
    ).fillna(1.0)
    market_data["Sentiment_Label"] = market_data.apply(
        lambda row: calculate_sentiment_label(row["Daily_Return"], float(row["Volume_Ratio"])),
        axis=1,
    )

    csv_output = data_dir / "ftspf_market_data.csv"
    market_data.to_csv(csv_output, index=False)

    summary = compute_financial_summary(market_data)
    summary_rows = [
        {"metric": key, "value": value} for key, value in summary.items() if key != "latest_prices"
    ]
    pd.DataFrame(summary_rows).to_csv(data_dir / "ftspf_financial_summary.csv", index=False)

    return market_data


def build_power_bi_exports(input_csv: str | Path, output_dir: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    source = Path(input_csv)
    market_data = pd.read_csv(source)
    if output_dir is None:
        output_dir = source.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = compute_financial_summary(market_data)
    summary_rows = [
        {"metric": key, "value": value} for key, value in summary.items() if key != "latest_prices"
    ]
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(output_dir / "ftspf_powerbi_summary.csv", index=False)

    daily_table = market_data.copy()
    daily_table["Date"] = pd.to_datetime(daily_table["Date"])
    daily_table.to_csv(output_dir / "ftspf_powerbi_daily_prices.csv", index=False)

    return market_data, summary_df


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    market_df = fetch_stock_market_data(output_dir=data_dir)
    insight_rows = generate_business_insights(market_df)
    market_df.to_csv(data_dir / "ftspf_market_data.csv", index=False)

    print("FTSPF dataset generated successfully.")
    print(f"Rows: {len(market_df)}")
    print(f"Stocks: {market_df['Company'].nunique()}")
    print(f"Latest date: {market_df['Date'].max()}")
    print(f"Sample insights: {insight_rows[:2]}")


if __name__ == "__main__":
    main()
