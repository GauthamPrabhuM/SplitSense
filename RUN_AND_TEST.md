# How to Run and Test SplitSense

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Option A: Use the setup script
./setup.sh

# Option B: Manual installation
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload
```

The application will be available at:
- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### Step 3: Test the Application

#### Option A: Using the Web Dashboard (Easiest)

1. Open http://localhost:8000 in your browser
2. You'll see the dashboard interface
3. To ingest data, you have two options:

   **Option 1: Using Splitwise API Token**
   - Get your token from https://secure.splitwise.com/apps
   - Enter it in the "Splitwise API Token" field
   - Click "Ingest Data"

   **Option 2: Using Exported File**
   - Export your Splitwise data as CSV or JSON
   - Click "Choose File" and select your export
   - Click "Ingest Data"

4. Once data is ingested, you'll see:
   - Summary cards with key metrics
   - Interactive charts (spending trends, balance trends, etc.)
   - Detailed insights

#### Option B: Using the API Directly

**Test Health Endpoint:**
```bash
curl http://localhost:8000/api/health
```

**Ingest Data via API:**
```bash
# Using API token
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{"api_token": "YOUR_TOKEN_HERE", "base_currency": "USD"}'

# Using file upload
curl -X POST "http://localhost:8000/api/ingest/file" \
  -F "file=@/path/to/your/export.csv" \
  -F "base_currency=USD"
```

**Get Insights:**
```bash
curl http://localhost:8000/api/insights
```

**Export CSV:**
```bash
curl http://localhost:8000/api/export/csv -o insights.csv
```

#### Option C: Using Python Script

```bash
# Set your API token (optional)
export SPLITWISE_API_TOKEN=your_token_here

# Run the example script
python example_usage.py
```

## 🧪 Running Unit Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_analytics.py -v
pytest tests/test_validation.py -v
```

## 📊 Testing Without Real Data

If you don't have a Splitwise account or want to test without real data, you can:

1. **Create Mock Data**: Create a simple JSON file with sample expenses
2. **Use Test Fixtures**: The test files contain sample data structures you can reference
3. **Test Individual Components**: Run tests which use mock data

### Example Mock Data Structure

Create a file `test_data.json`:
```json
{
  "expenses": [
    {
      "id": 1,
      "group_id": 1,
      "description": "Test Expense",
      "payment": false,
      "cost": "50.00",
      "currency_code": "USD",
      "date": "2024-01-15T00:00:00Z",
      "created_by": {
        "id": 1,
        "first_name": "Test",
        "last_name": "User"
      },
      "users": [
        {
          "user": {"id": 1, "first_name": "Test"},
          "paid_share": "50.00",
          "owed_share": "25.00"
        },
        {
          "user": {"id": 2, "first_name": "Friend"},
          "paid_share": "0.00",
          "owed_share": "25.00"
        }
      ],
      "repayments": [],
      "category": "Food & Drink"
    }
  ],
  "groups": [
    {
      "id": 1,
      "name": "Test Group",
      "group_type": "other",
      "updated_at": "2024-01-15T00:00:00Z",
      "members": []
    }
  ],
  "current_user": {
    "id": 1,
    "first_name": "Test",
    "last_name": "User"
  }
}
```

Then upload it via the dashboard or API.

## 🔍 Testing Checklist

- [ ] Application starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Dashboard loads correctly
- [ ] Can ingest data via API token
- [ ] Can ingest data via file upload
- [ ] Insights are generated correctly
- [ ] Charts render properly
- [ ] CSV export works
- [ ] PDF export works
- [ ] Unit tests pass
- [ ] Validation checks work correctly

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### API Token Issues
- Verify token is correct at https://secure.splitwise.com/apps
- Check token hasn't expired
- Ensure token has necessary permissions

### File Upload Issues
- Check file format (CSV or JSON)
- Verify file encoding is UTF-8
- Check file size (should be reasonable)

## 📝 Example Test Session

```bash
# 1. Start the server
uvicorn main:app --reload

# 2. In another terminal, test health
curl http://localhost:8000/api/health

# 3. Run unit tests
pytest tests/ -v

# 4. Open dashboard
# Visit http://localhost:8000 in browser

# 5. Test with your Splitwise data
# Use the dashboard to ingest and view insights
```

## 🎯 Next Steps After Testing

1. Review the generated insights
2. Check validation results for data integrity
3. Explore different visualizations
4. Export reports (CSV/PDF)
5. Review unit test coverage
6. Customize analytics if needed

