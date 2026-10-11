# Data sources and provenance

## Source repository

The upstream repository used as the base for this project is:

- https://github.com/bnithinchandra-dotcom/PowerBI-Stock-Market-Analytics

The original project is a stock-market analytics dashboard built with Python and Power BI. This FTSPF project preserves the useful stock-data workflow and repackages it for a financial trend and sentiment mini-project.

## Market data source

The live market data is fetched via Yahoo Finance using the Python package `yfinance`.

Selected symbols include:

- AAPL
- MSFT
- NVDA
- AMZN
- GOOGL
- META
- TSLA
- NFLX
- JPM
- WMT

The default time window is from 2020-01-01 to the current date, with the window configurable in the pipeline code.

## Licence and usage status

The upstream repository inspected in this workspace did not include a dedicated `LICENSE` file. Because of that, no additional licence claim is made beyond preserving attribution to the original repository and using the project as an educational, non-commercial adaptation.

## Sentiment data status

The repository does not include a labelled sentiment dataset or a trained sentiment model. The sentiment layer is therefore implemented as a transparent rule-based fallback using:

- daily return direction,
- relative trading volume changes,
- a `Positive` / `Negative` / `Neutral` label generated from those rules.

This is not a trained AI or forecasting model and should be interpreted as a demonstration of BI-style market sentiment proxying rather than a genuine sentiment prediction system.

## Limitations

- Yahoo Finance data is market data, not a research-grade sentiment dataset.
- The sentiment fallback is heuristic, not trained on labelled headlines or social data.
- The project does not claim future-price prediction.
- Power BI output depends on the CSV files exported by the Python workflow.
