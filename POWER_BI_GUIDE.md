# Power BI guide

## Importing FTSPF data into Power BI Desktop

1. Open Power BI Desktop.
2. Select Get Data.
3. Choose Text/CSV.
4. Import the file `data/ftspf_market_data.csv`.
5. Confirm the data types for:
   - `Date` as Date
   - `Company` as Text
   - `Open`, `High`, `Low`, `Close`, `Volume`, `Daily_Return`, `Volume_Ratio` as Decimal/Whole Number where appropriate
6. Create relationships if you use multiple tables.

## Recommended visuals

- KPI cards: total records, number of companies, latest price, average volume
- Line chart: closing price by date and company
- Bar chart: average daily return by company
- Column chart: trading volume by company
- Matrix: sentiment distribution by stock and day
- Scatter or combo chart: sentiment proxy vs. close price movement

## Suggested filters

- Company
- Date range
- Sentiment label

## Refreshing the data

When the source data changes, re-run:

```bash
python src/ftspf_framework.py
```

Then in Power BI, use Refresh to load the updated CSV files.

## Report notes

- No source `.pbix` file is included in this repository.
- The project provides clean CSV exports for a Power BI build rather than a bundled binary report.
- If Power BI Desktop is not installed, the CSV exports can still be used in a later report build.
