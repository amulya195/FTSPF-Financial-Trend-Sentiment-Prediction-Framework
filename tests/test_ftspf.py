from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ftspf_framework import (  # noqa: E402
    calculate_sentiment_label,
    compute_financial_summary,
    generate_business_insights,
)


def test_calculate_sentiment_label():
    assert calculate_sentiment_label(0.025, 1.2) == "Positive"
    assert calculate_sentiment_label(-0.015, 0.9) == "Negative"
    assert calculate_sentiment_label(0.002, 1.0) == "Neutral"


def test_compute_financial_summary():
    df = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-02"],
            "Company": ["AAPL", "AAPL"],
            "Close": [100.0, 110.0],
            "Volume": [50_000, 60_000],
            "Daily_Return": [0.0, 0.1],
        }
    )

    summary = compute_financial_summary(df)
    assert summary["total_records"] == 2
    assert summary["selected_stocks"] == 1
    assert summary["latest_price"] == 110.0
    assert summary["average_volume"] == 55_000.0


def test_generate_business_insights():
    df = pd.DataFrame(
        {
            "Company": ["AAPL", "MSFT"],
            "Sentiment_Label": ["Positive", "Negative"],
            "Daily_Return": [0.02, -0.01],
            "Close": [110.0, 150.0],
        }
    )
    insights = generate_business_insights(df)
    assert len(insights) > 0
    assert any("Sentiment" in insight for insight in insights)
