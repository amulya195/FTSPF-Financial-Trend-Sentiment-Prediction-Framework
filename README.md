# FTSPF – Financial Trend Sentiment Prediction Framework

FTSPF is a college-level Business Intelligence mini-project that adapts the original stock market analytics workflow into a cleaner financial dashboard focused on trend monitoring, KPI review, and a transparent sentiment fallback layer.

This project preserves the useful stock-data collection and Power BI-friendly export workflow from the source repository while reframing the narrative around a practical, audit-friendly framework for financial trend and sentiment analysis.

## Project purpose

The goal is to demonstrate how a small BI workflow can:

- collect historical market data for major technology and retail stocks,
- compute key performance indicators such as returning prices and trading volume,
- apply a clearly labelled sentiment proxy when no genuine sentiment dataset or predictive model is available,
- export clean CSV data for Power BI exploration,
- present concise business insights based on the observed market behaviour.

## Project status

This repository currently includes:

- a reusable Python pipeline for stock-data ingestion and cleaning,
- a rule-based sentiment fallback that is explicitly labelled as a proxy rather than a trained model,
- CSV exports suitable for Power BI import,
- documentation for data provenance, Power BI usage, and presentation guidance.


## Business intelligence features

- Financial overview dashboard KPIs
- Selected-stock tracking and latest price review
- Price trend and return analysis
- Volume trend comparison
- Sentiment proxy by stock-day using daily return and volume behaviour
- Business insight summary prompts
- Clean CSV exports for Power BI

## Sentiment note

A labelled sentiment dataset or trained predictive model is not included in this repository.

To keep the project honest and testable, FTSPF uses a transparent rule-based sentiment fallback derived from:

- daily return direction,
- relative trading volume change,
- explicit flagging as a sentiment proxy rather than AI prediction.

This is suitable for academic demonstration, but it is not a genuine market sentiment model.

## Tech stack

- Python 3.11+
- pandas
- yfinance
- NumPy
- Power BI
- CSV data exports

## Project structure

```text
FTSPF-Financial-Trend-Sentiment-Prediction-Framework/
├── README.md
├── requirements.txt
├── .gitignore
├── DATA_SOURCES.md
├── POWER_BI_GUIDE.md
├── PRESENTATION_GUIDE.md
├── src/
│   └── ftspf_framework.py
├── tests/
│   └── test_ftspf.py
├── data/
│   ├── ftspf_market_data.csv
│   ├── ftspf_financial_summary.csv
│   └── ftspf_powerbi_summary.csv
├── assets/
│   └── screenshots and exported visuals
└── FTSPF_Stock_Market_Analytics.ipynb
```

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment if desired.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the project

```bash
python src/ftspf_framework.py
```

This generates the cleaned stock-market dataset and summary exports under the `data/` directory.

## Run tests

```bash
pytest -q
```

## Power BI workflow

The project exports data into CSV files that can be imported directly into Power BI Desktop. For detailed steps, see [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md).

## Data sources

See [DATA_SOURCES.md](DATA_SOURCES.md) for the dataset origin, provenance, and limitations.

## Presentation guidance

See [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) for a short project brief suitable for a mini-project demo.

## Screenshots

The original project contains dashboard screenshots and a demo video in the upstream repository. These assets can be kept as reference materials for a presentation or report.

## Repository details

- Project name: FTSPF – Financial Trend Sentiment Prediction Framework
- Target repository: https://github.com/amulya195/FTSPF-Financial-Trend-Sentiment-Prediction-Framework
- Source reference: https://github.com/bnithinchandra-dotcom/PowerBI-Stock-Market-Analytics

## Notes

- No future-price prediction claims are made in this project.
- No secrets, API keys, or private credentials are stored in the repository.
- The sentiment layer is intentionally transparent and clearly marked as a rule-based fallback.
