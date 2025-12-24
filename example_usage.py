"""
Example usage of the Splitwise Analysis Tool.
"""
import os
from ingestion import SplitwiseAPIClient, FileParser, DataNormalizer
from validation import DataVerifier
from analytics import (
    SpendingAnalyzer,
    BalanceAnalyzer,
    CategoryAnalyzer,
    GroupAnalyzer,
    AdvancedAnalyzer,
)
from models.schemas import AllInsights


def analyze_from_api(api_token: str, base_currency: str = "USD"):
    """Example: Analyze data from Splitwise API"""
    print("Fetching data from Splitwise API...")
    
    # Fetch data
    client = SplitwiseAPIClient(api_token)
    data = client.fetch_all_data()
    
    # Parse data
    current_user_id = data["current_user"].get("id", 1)
    groups = [client.parse_group(g) for g in data.get("groups", [])]
    expenses = [client.parse_expense(e) for e in data.get("expenses", [])]
    
    print(f"Fetched {len(expenses)} expenses and {len(groups)} groups")
    
    # Process data
    insights = process_data(expenses, groups, current_user_id, base_currency)
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total Spending: {insights.spending.total_spending:,.2f} {insights.spending.currency_code}")
    print(f"Net Balance: {insights.balance.net_balance:,.2f} {insights.balance.currency_code}")
    print(f"Validation: {'✓ Valid' if insights.validation.is_valid else '✗ Invalid'}")
    if insights.validation.errors:
        print(f"Errors: {len(insights.validation.errors)}")
    if insights.validation.warnings:
        print(f"Warnings: {len(insights.validation.warnings)}")
    
    return insights


def analyze_from_file(file_path: str, base_currency: str = "USD"):
    """Example: Analyze data from exported file"""
    print(f"Parsing data from {file_path}...")
    
    # Parse file
    parser = FileParser()
    data = parser.parse(file_path)
    
    # Extract data (format depends on file type)
    if isinstance(data, dict):
        current_user_id = data.get("current_user", {}).get("id", 1)
        
        # Parse groups and expenses
        client = SplitwiseAPIClient("dummy")  # Won't be used for API calls
        groups = [client.parse_group(g) for g in data.get("groups", [])]
        expenses = [client.parse_expense(e) for e in data.get("expenses", [])]
    else:
        raise ValueError("Unexpected file format")
    
    print(f"Parsed {len(expenses)} expenses and {len(groups)} groups")
    
    # Process data
    insights = process_data(expenses, groups, current_user_id, base_currency)
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total Spending: {insights.spending.total_spending:,.2f} {insights.spending.currency_code}")
    print(f"Net Balance: {insights.balance.net_balance:,.2f} {insights.balance.currency_code}")
    
    return insights


def process_data(expenses, groups, current_user_id, base_currency):
    """Process data and generate insights"""
    from main import process_data as _process_data
    return _process_data(expenses, groups, current_user_id, base_currency)


if __name__ == "__main__":
    # Example 1: Using API token
    api_token = os.getenv("SPLITWISE_API_TOKEN")
    if api_token:
        print("=== Example 1: API Analysis ===")
        insights = analyze_from_api(api_token)
    else:
        print("SPLITWISE_API_TOKEN not set. Skipping API example.")
    
    # Example 2: Using file (uncomment and provide path)
    # print("\n=== Example 2: File Analysis ===")
    # insights = analyze_from_file("path/to/export.csv")

