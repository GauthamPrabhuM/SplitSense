# Quick Start Guide

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd SplitWiseAnalysisTool
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```
   
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Web Dashboard (Recommended)

1. **Start the server**
   ```bash
   source venv/bin/activate  # if not already activated
   uvicorn main:app --reload
   ```

2. **Open your browser**
   - Navigate to `http://localhost:8000`
   - Use the dashboard to ingest data and view insights

3. **Ingest data via dashboard**
   - Enter your Splitwise API token, OR
   - Upload a CSV/JSON export file

### Option 2: Command Line / Python Script

1. **Set your API token (optional)**
   ```bash
   export SPLITWISE_API_TOKEN=your_token_here
   ```

2. **Run the example script**
   ```bash
   python example_usage.py
   ```

### Option 3: API Endpoints

1. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Use the API**
   - Health check: `GET http://localhost:8000/api/health`
   - Ingest data: `POST http://localhost:8000/api/ingest`
   - Get insights: `GET http://localhost:8000/api/insights`
   - Export CSV: `GET http://localhost:8000/api/export/csv`
   - Export PDF: `GET http://localhost:8000/api/export/pdf`

   See `http://localhost:8000/docs` for interactive API documentation.

## Getting Your Splitwise API Token

1. Go to [Splitwise Developer Settings](https://secure.splitwise.com/apps)
2. Click "Create new app"
3. Fill in the form (name, description, etc.)
4. Copy the "Personal Access Token"
5. Use this token in the dashboard or set it as `SPLITWISE_API_TOKEN` environment variable

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

## Troubleshooting

### Import Errors
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

### API Errors
- Verify your API token is correct
- Check that you have internet connectivity
- Splitwise API has rate limits - wait a moment and try again

### File Parsing Errors
- Ensure your CSV/JSON file matches Splitwise export format
- Check file encoding (should be UTF-8)

## Next Steps

- Review the [README.md](README.md) for detailed documentation
- Check the [example_usage.py](example_usage.py) for code examples
- Explore the dashboard at `http://localhost:8000`

