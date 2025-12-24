# Splitwise Analysis Tool

A comprehensive tool for analyzing Splitwise account data with accurate, verifiable insights.

## Features

- **Data Ingestion**: Support for Splitwise REST API and CSV/JSON exports
- **Data Integrity**: Cross-verification of totals and detection of inconsistencies
- **Analytics**: Spending trends, balance analysis, category breakdowns, group insights
- **Advanced Insights**: Anomaly detection, subscription identification, balance predictions
- **Interactive Dashboard**: Web-based visualization of all insights
- **Exportable Reports**: CSV and PDF export functionality

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### Using Splitwise API

1. Get your personal access token from [Splitwise Developer Settings](https://secure.splitwise.com/apps)
2. Set environment variable: `export SPLITWISE_API_TOKEN=your_token_here`
3. Or pass it via the API/CLI

### Using Exported Data

Export your Splitwise data as CSV or JSON and provide the file path.

## Usage

### Web Dashboard

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` for the interactive dashboard.

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/ingest` - Ingest data (API token or file upload)
- `GET /api/insights` - Get all insights
- `GET /api/export/csv` - Export insights as CSV
- `GET /api/export/pdf` - Export insights as PDF

## Project Structure

```
SplitWiseAnalysisTool/
├── main.py                 # FastAPI application
├── ingestion/              # Data ingestion layer
│   ├── __init__.py
│   ├── api_client.py       # Splitwise API client
│   ├── file_parser.py      # CSV/JSON parser
│   └── normalizer.py       # Currency/timestamp normalization
├── models/                 # Data models
│   ├── __init__.py
│   └── schemas.py          # Pydantic models
├── analytics/              # Analytics engine
│   ├── __init__.py
│   ├── spending.py         # Spending analysis
│   ├── balances.py         # Balance analysis
│   ├── categories.py        # Category analysis
│   └── advanced.py         # Advanced insights
├── validation/             # Data integrity checks
│   ├── __init__.py
│   └── verifier.py         # Cross-verification logic
├── visualization/          # Dashboard components
│   ├── __init__.py
│   └── charts.py           # Plotly visualizations
├── storage/                # Optional storage layer
│   ├── __init__.py
│   └── db.py               # DuckDB storage
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_analytics.py
│   └── test_validation.py
└── templates/              # HTML templates
    └── dashboard.html
```

## Assumptions & Limitations

### Assumptions

1. **Currency Handling**: All amounts are normalized to a base currency (USD by default). Multi-currency expenses are converted using exchange rates at transaction time.
2. **Settlement Detection**: Settlements are identified by zero-sum transactions or explicit settlement markers.
3. **Category Mapping**: Categories are mapped from Splitwise's category system. Unmapped categories are labeled as "Other".
4. **Time Zones**: All timestamps are normalized to UTC for consistency.

### Limitations

1. **API Rate Limits**: Splitwise API has rate limits. The tool handles pagination but may take time for large datasets.
2. **Historical Exchange Rates**: Currency conversion uses rates at transaction time. Historical rate accuracy depends on Splitwise's data.
3. **Deleted Expenses**: Expenses deleted in Splitwise may not appear in exports, affecting historical accuracy.
4. **Partial Data**: If API access is limited, insights are based only on available data.

## Correctness Checks

The tool performs the following validation checks:

1. **Balance Verification**: Sum of all group balances should equal zero
2. **Expense Totals**: Sum of paid amounts should equal sum of owed amounts for each expense
3. **Net Balance**: Personal net balance should match sum of all group balances
4. **Settlement Integrity**: Settlement transactions should balance to zero
5. **Currency Consistency**: All amounts in a group should use the same currency

Validation results are included in the insights output.

## Security & Privacy

- **Token Storage**: API tokens are never stored unless explicitly enabled via configuration
- **Local Execution**: All processing happens locally; no data is sent to external services
- **Data Masking**: Sensitive information (names, amounts) can be masked in logs via configuration
- **No Persistent Storage**: By default, data is processed in-memory. Optional SQLite/DuckDB storage can be enabled.

## Testing

```bash
pytest tests/ -v --cov=.
```

## License

MIT

