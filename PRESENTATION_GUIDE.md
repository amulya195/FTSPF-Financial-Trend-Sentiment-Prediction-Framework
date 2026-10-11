# Presentation guide

## Problem statement

Traditional market dashboards often focus on price movement and volume without connecting the results to a clear business narrative. FTSPF addresses this gap by combining stock-price analytics with a transparent sentiment proxy and executive-friendly insights.

## Objectives

- Review historical stock performance for major companies
- Highlight financial KPIs and trend direction
- Compare market behaviour with a simplified sentiment measure
- Present insights in a way that is easy to explain in a BI presentation

## Methodology

1. Fetch stock market data using `yfinance`.
2. Clean and standardize tables for analysis.
3. Compute daily return, volume ratios, and sentiment labels.
4. Summarize the data into KPIs and business insight statements.
5. Export CSV files for Power BI import.

## Architecture

```text
yfinance data collection
        ↓
Python cleaning and transformation
        ↓
FTSPF KPI and sentiment calculations
        ↓
CSV exports for Power BI
        ↓
Business-insight narrative and dashboard visuals
```

## Business insights example

- Positive sentiment is dominant when there is a combination of positive daily return and increased volume.
- Negative sentiment may suggest weaker momentum or risk-off behaviour.
- Price and volume behaviour are more informative than raw close prices alone when explaining market activity.

## Limitations

- The sentiment layer is a proxy, not a trained sentiment model.
- The project does not attempt to predict future prices.
- The data source is market-price data rather than a dedicated consumer-sentiment dataset.

## Demo steps

1. Run the pipeline:
   ```bash
   python src/ftspf_framework.py
   ```
2. Inspect the exported CSV files in `data/`.
3. Import `ftspf_market_data.csv` into Power BI.
4. Build visuals using the recommended KPI and trend charts.
5. Present the business insight summary alongside the stock movement visuals.
