"""
FastAPI application for Splitwise Analysis Tool.
"""
import os
import tempfile
from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ingestion import SplitwiseAPIClient, FileParser, DataNormalizer
from validation import DataVerifier
from analytics import (
    SpendingAnalyzer,
    BalanceAnalyzer,
    CategoryAnalyzer,
    GroupAnalyzer,
    AdvancedAnalyzer,
)
from visualization import ChartGenerator
from models.schemas import (
    Expense,
    Group,
    AllInsights,
    ExpenseData,
    GroupData,
    UserData,
)
from config import Config

app = FastAPI(title="Splitwise Analysis Tool", version="1.0.0")

# Global state (in production, use proper state management)
current_data: Optional[AllInsights] = None
current_expenses: list[Expense] = []
current_groups: list[Group] = []
current_user_id: Optional[int] = None
current_friend_balances: list[dict] = []  # Friend balances from Splitwise API


class IngestRequest(BaseModel):
    """Request model for data ingestion"""
    api_token: Optional[str] = None
    base_currency: str = "USD"


def mask_sensitive_data(text: str, mask_char: str = "*") -> str:
    """Mask sensitive information in logs"""
    return Config.mask_sensitive_data(text, mask_char)


def process_data(
    expenses: list[Expense],
    groups: list[Group],
    current_user_id: int,
    base_currency: str = "USD"
) -> AllInsights:
    """Process data and generate all insights"""
    # Detect original currency from RAW expenses BEFORE normalization
    # This ensures we show the actual currency from Splitwise API, not normalized USD
    from collections import Counter
    if expenses:
        # Get currency from raw expenses (before normalization)
        # These expenses still have their original currency_code from Splitwise
        currency_counts = Counter(e.currency_code for e in expenses if not e.deleted_at and e.currency_code)
        if currency_counts:
            original_currency = currency_counts.most_common(1)[0][0]
            print(f"Detected original currency: {original_currency} (from {currency_counts[original_currency]} expenses)")
        else:
            # Fallback: try to get from first expense
            original_currency = expenses[0].currency_code if expenses and expenses[0].currency_code else base_currency
    else:
        original_currency = base_currency
    
    print(f"Using currency: {original_currency} (base: {base_currency})")
    
    # Normalize data
    normalizer = DataNormalizer(base_currency=base_currency)
    normalized_expenses = normalizer.normalize_expenses(expenses)
    normalized_groups = normalizer.normalize_groups(groups)
    
    # Validate data
    verifier = DataVerifier(current_user_id=current_user_id)
    validation = verifier.verify_all(normalized_expenses, normalized_groups)
    
    # Run analytics
    spending_analyzer = SpendingAnalyzer(current_user_id)
    spending = spending_analyzer.analyze(normalized_expenses)
    
    balance_analyzer = BalanceAnalyzer(current_user_id)
    balance = balance_analyzer.analyze(normalized_expenses)
    
    category_analyzer = CategoryAnalyzer(current_user_id)
    categories = category_analyzer.analyze(normalized_expenses)
    
    group_analyzer = GroupAnalyzer(current_user_id)
    groups_insight = group_analyzer.analyze(normalized_expenses, normalized_groups)
    
    advanced_analyzer = AdvancedAnalyzer(current_user_id)
    anomalies = advanced_analyzer.detect_anomalies(normalized_expenses)
    subscriptions = advanced_analyzer.detect_subscriptions(normalized_expenses)
    settlement = advanced_analyzer.analyze_settlement_efficiency(normalized_expenses)
    cash_flow = advanced_analyzer.analyze_cash_flow(normalized_expenses)
    prediction = advanced_analyzer.predict_balance(normalized_expenses)
    friction = advanced_analyzer.rank_friction(normalized_expenses, normalized_groups)
    
    # Get recurring expenses from subscriptions
    recurring = subscriptions.subscriptions
    
    # Data summary
    data_summary = {
        "total_expenses": len(normalized_expenses),
        "total_groups": len(normalized_groups),
        "date_range": {
            "earliest": min((e.date for e in normalized_expenses), default=None),
            "latest": max((e.date for e in normalized_expenses), default=None),
        },
        "currencies": list(set(e.currency_code for e in normalized_expenses)),
        "original_currency": original_currency,
        "base_currency": base_currency,
    }
    
    # ALWAYS use original currency for display (don't normalize to USD)
    # Only normalize internally for calculations, but display in original currency
    if original_currency != base_currency and original_currency in normalizer.EXCHANGE_RATES:
        # Convert back to original currency for display
        conversion_rate = normalizer.EXCHANGE_RATES[base_currency] / normalizer.EXCHANGE_RATES[original_currency]
        
        # Update spending insight - convert back to original currency
        spending.total_spending = spending.total_spending * conversion_rate
        spending.currency_code = original_currency
        spending.monthly_breakdown = {k: float(v * conversion_rate) for k, v in spending.monthly_breakdown.items()}
        spending.quarterly_breakdown = {k: float(v * conversion_rate) for k, v in spending.quarterly_breakdown.items()}
        spending.yearly_breakdown = {k: float(v * conversion_rate) for k, v in spending.yearly_breakdown.items()}
        # Convert the new spending fields
        if spending.monthly_average is not None:
            spending.monthly_average = spending.monthly_average * conversion_rate
        if spending.peak_amount is not None:
            spending.peak_amount = spending.peak_amount * conversion_rate
        
        # Update balance insight
        balance.net_balance = balance.net_balance * conversion_rate
        balance.currency_code = original_currency
        balance.owed_to_user = balance.owed_to_user * conversion_rate
        balance.user_owes = balance.user_owes * conversion_rate
        balance.trend_over_time = {k: float(v * conversion_rate) for k, v in balance.trend_over_time.items()}
        # Convert per-person balances
        balance.by_person = {k: float(v * conversion_rate) for k, v in balance.by_person.items()}
        
        # Update category insight
        categories.currency_code = original_currency
        categories.by_category = {k: float(v * conversion_rate) for k, v in categories.by_category.items()}
        for cat in categories.top_categories:
            cat['amount'] = float(cat['amount']) * float(conversion_rate)
        
        # Update group insight
        groups_insight.currency_code = original_currency
        for group_id, group_data in groups_insight.by_group.items():
            group_data['total_spending'] = float(group_data['total_spending']) * float(conversion_rate)
        for group in groups_insight.top_groups:
            group['total_spending'] = float(group['total_spending']) * float(conversion_rate)
        
        # Update subscriptions
        subscriptions.currency_code = original_currency
        subscriptions.total_monthly_subscriptions = subscriptions.total_monthly_subscriptions * conversion_rate
        for sub in subscriptions.subscriptions:
            sub.average_amount = sub.average_amount * conversion_rate
            sub.total_amount = sub.total_amount * conversion_rate
        
        # Update cash flow
        cash_flow.currency_code = original_currency
        cash_flow.total_paid = cash_flow.total_paid * conversion_rate
        cash_flow.total_received = cash_flow.total_received * conversion_rate
        cash_flow.net_cash_flow = cash_flow.net_cash_flow * conversion_rate
        
        # Update settlement efficiency
        settlement.currency_code = original_currency
        settlement.unpaid_balances_total = settlement.unpaid_balances_total * conversion_rate
        
        # Update balance prediction
        prediction.currency_code = original_currency
        prediction.predicted_balance = prediction.predicted_balance * conversion_rate
        
        # Update anomalies - convert amounts and regenerate reason strings
        for anomaly in anomalies.anomalies:
            # Parse the original threshold from reason string and convert
            old_amount = anomaly['amount']
            anomaly['amount'] = float(old_amount) * float(conversion_rate)
            # Update the reason string with converted values
            if 'reason' in anomaly and 'exceeds threshold' in anomaly['reason']:
                # Extract and convert threshold from reason
                import re
                match = re.search(r'threshold \(([0-9,.]+)\)', anomaly['reason'])
                if match:
                    old_threshold = float(match.group(1).replace(',', ''))
                    new_threshold = old_threshold * float(conversion_rate)
                    anomaly['reason'] = f"Amount ({anomaly['amount']:,.2f}) exceeds threshold ({new_threshold:,.2f})"
        
        # Update friction - convert unpaid_balance for each person
        for person in friction.by_person:
            person['unpaid_balance'] = float(person['unpaid_balance']) * float(conversion_rate)
            person['friction_score'] = float(person['friction_score']) * float(conversion_rate)
        for group in friction.by_group:
            group['unpaid_balance'] = float(group['unpaid_balance']) * float(conversion_rate)
            group['friction_score'] = float(group['friction_score']) * float(conversion_rate)
    else:
        # If already in original currency, just update currency codes
        spending.currency_code = original_currency
        balance.currency_code = original_currency
        categories.currency_code = original_currency
        groups_insight.currency_code = original_currency
        subscriptions.currency_code = original_currency
        cash_flow.currency_code = original_currency
        settlement.currency_code = original_currency
        prediction.currency_code = original_currency
    
    return AllInsights(
        validation=validation,
        spending=spending,
        balance=balance,
        categories=categories,
        groups=groups_insight,
        recurring=recurring,
        settlement_efficiency=settlement,
        cash_flow=cash_flow,
        anomalies=anomalies,
        subscriptions=subscriptions,
        balance_prediction=prediction,
        friction=friction,
        data_summary=data_summary,
    )


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML"""
    return read_dashboard_html()


def read_dashboard_html() -> str:
    """Read dashboard HTML template"""
    try:
        with open("templates/dashboard.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Return basic HTML if template doesn't exist
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Splitwise Analysis Tool</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #333; }
                .section { margin: 30px 0; padding: 20px; background: #f5f5f5; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Splitwise Analysis Tool</h1>
                <p>Please ingest data first using POST /api/ingest</p>
                <p>Or visit <a href="/docs">/docs</a> for API documentation.</p>
            </div>
        </body>
        </html>
        """


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/api/ingest")
async def ingest_data(request: IngestRequest):
    """
    Ingest data from Splitwise API or file upload.
    
    Supports:
    - API token (via request body)
    - File upload (via multipart form)
    """
    global current_data, current_expenses, current_groups, current_user_id, current_friend_balances
    
    expenses = []
    groups = []
    user_id = None
    friend_balances = []
    
    # Try API token first
    if request.api_token:
        try:
            # Mask token in logs
            masked_token = mask_sensitive_data(request.api_token)
            print(f"Ingesting data from API (token: {masked_token})")
            
            client = SplitwiseAPIClient(request.api_token)
            data = client.fetch_all_data()
            
            # Parse data
            current_user_id = data["current_user"].get("id", 1)
            user_id = current_user_id
            
            # Fetch friend balances directly from Splitwise API
            try:
                friends_data = client.get_friends()
                for friend in friends_data:
                    # Each friend has a 'balance' array with currency-specific balances
                    balances = friend.get("balance", [])
                    for bal in balances:
                        amount = float(bal.get("amount", 0))
                        if amount != 0:  # Only include non-zero balances
                            friend_balances.append({
                                "user_id": friend.get("id"),
                                "first_name": friend.get("first_name", ""),
                                "last_name": friend.get("last_name", ""),
                                "email": friend.get("email"),
                                "balance": amount,  # Positive = they owe you
                                "currency_code": bal.get("currency_code", "USD")
                            })
                print(f"Fetched {len(friend_balances)} friend balances")
            except Exception as e:
                print(f"Warning: Failed to fetch friend balances: {str(e)}")
            
            # Parse groups with error handling
            for idx, group_data in enumerate(data.get("groups", [])):
                try:
                    groups.append(client.parse_group(group_data))
                except Exception as e:
                    print(f"Warning: Failed to parse group at index {idx}: {str(e)}")
                    continue  # Skip invalid groups
            
            # Parse expenses with error handling
            for idx, expense_data in enumerate(data.get("expenses", [])):
                try:
                    expenses.append(client.parse_expense(expense_data))
                except Exception as e:
                    print(f"Warning: Failed to parse expense at index {idx}: {str(e)}")
                    continue  # Skip invalid expenses
            
        except Exception as e:
            error_msg = str(e)
            # Provide more helpful error messages
            if "validation error" in error_msg.lower():
                error_msg = f"Data validation error: {error_msg}. This may be due to missing or invalid user IDs in the API response."
            raise HTTPException(status_code=400, detail=f"API ingestion failed: {error_msg}")
    
    # Process data
    if expenses:
        current_expenses = expenses
        current_groups = groups
        current_user_id = user_id or 1
        current_friend_balances = friend_balances  # Store friend balances
        
        insights = process_data(
            expenses,
            groups,
            current_user_id,
            request.base_currency
        )
        current_data = insights
        
        return {
            "status": "success",
            "expenses_count": len(expenses),
            "groups_count": len(groups),
            "current_user_id": current_user_id,
            "friend_balances_count": len(friend_balances),
        }
    else:
        raise HTTPException(status_code=400, detail="No data ingested. Provide API token or upload file.")


@app.post("/api/ingest/file")
async def ingest_file(
    file: UploadFile = File(...),
    base_currency: str = Form("USD")
):
    """
    Ingest data from uploaded file (CSV or JSON).
    """
    global current_data, current_expenses, current_groups, current_user_id
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Parse file
        parser = FileParser()
        data = parser.parse(tmp_path)
        
        # Extract data (format depends on file type)
        if isinstance(data, dict):
            # API-like format
            current_user_id = data.get("current_user", {}).get("id", 1)
            
            # Parse groups (if in API format)
            if "groups" in data and isinstance(data["groups"], list):
                if data["groups"] and isinstance(data["groups"][0], dict):
                    # Need to parse
                    client = SplitwiseAPIClient("dummy")  # Won't be used
                    groups = [client.parse_group(g) for g in data["groups"]]
                else:
                    groups = data["groups"]
            else:
                groups = []
            
            # Parse expenses (if in API format)
            if "expenses" in data and isinstance(data["expenses"], list):
                if data["expenses"] and isinstance(data["expenses"][0], dict):
                    client = SplitwiseAPIClient("dummy")
                    expenses = [client.parse_expense(e) for e in data["expenses"]]
                else:
                    expenses = data["expenses"]
            else:
                expenses = []
        else:
            raise ValueError("Unexpected file format")
        
        current_expenses = expenses
        current_groups = groups
        current_user_id = current_user_id or 1
        
        # Process data
        insights = process_data(
            expenses,
            groups,
            current_user_id,
            base_currency
        )
        current_data = insights
        
        return {
            "status": "success",
            "expenses_count": len(expenses),
            "groups_count": len(groups),
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parsing failed: {str(e)}")
    
    finally:
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass


@app.get("/api/insights")
async def get_insights():
    """Get all generated insights"""
    if current_data is None:
        raise HTTPException(status_code=404, detail="No data available. Please ingest data first.")
    
    return current_data.model_dump()


@app.get("/api/friends")
async def get_friends():
    """Get friend balances from Splitwise API (accurate current balances)"""
    if not current_friend_balances:
        raise HTTPException(status_code=404, detail="No friend data available. Please ingest data first.")
    
    return {"friends": current_friend_balances}


@app.get("/api/insights/charts")
async def get_charts():
    """Get all charts as HTML"""
    if current_data is None:
        raise HTTPException(status_code=404, detail="No data available. Please ingest data first.")
    
    charts = ChartGenerator.generate_all_charts(current_data)
    return charts


@app.get("/api/export/csv")
async def export_csv():
    """Export insights as CSV"""
    if current_data is None:
        raise HTTPException(status_code=404, detail="No data available.")
    
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write spending data
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Spending", current_data.spending.total_spending])
    writer.writerow(["Net Balance", current_data.balance.net_balance])
    writer.writerow([])
    
    # Write monthly breakdown
    writer.writerow(["Month", "Spending"])
    for month, amount in current_data.spending.monthly_breakdown.items():
        writer.writerow([month, amount])
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(output.getvalue())
        tmp_path = f.name
    
    return FileResponse(
        tmp_path,
        media_type='text/csv',
        filename='splitwise_insights.csv'
    )


@app.get("/api/export/pdf")
async def export_pdf():
    """Export insights as PDF"""
    if current_data is None:
        raise HTTPException(status_code=404, detail="No data available.")
    
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_path = tmp_file.name
    
    c = canvas.Canvas(tmp_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Splitwise Analysis Report")
    
    y = height - 100
    
    # Spending summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Spending Summary")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Total Spending: {current_data.spending.total_spending:,.2f} {current_data.spending.currency_code}")
    y -= 15
    c.drawString(50, y, f"Net Balance: {current_data.balance.net_balance:,.2f} {current_data.balance.currency_code}")
    
    y -= 30
    
    # Top categories
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Top Categories")
    y -= 20
    c.setFont("Helvetica", 10)
    for cat in current_data.categories.top_categories[:5]:
        c.drawString(50, y, f"{cat['category']}: {cat['amount']:,.2f} ({cat['percentage']:.1f}%)")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50
    
    c.save()
    
    return FileResponse(
        tmp_path,
        media_type='application/pdf',
        filename='splitwise_insights.pdf'
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

