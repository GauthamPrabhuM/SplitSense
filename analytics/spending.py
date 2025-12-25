"""
Spending analysis module.
Analyzes total spending over time (monthly, quarterly, yearly).
"""
from typing import Dict, List
from decimal import Decimal
from collections import defaultdict
from datetime import datetime

from models.schemas import Expense, SpendingInsight


class SpendingAnalyzer:
    """Analyze spending trends over time"""
    
    def __init__(self, current_user_id: int):
        """
        Initialize analyzer.
        
        Args:
            current_user_id: ID of the current user
        """
        self.current_user_id = current_user_id
    
    def analyze(self, expenses: List[Expense]) -> SpendingInsight:
        """
        Analyze spending trends.
        
        Args:
            expenses: List of expenses
        
        Returns:
            SpendingInsight with breakdowns
        """
        # Filter out deleted expenses and settlements
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        # Calculate total spending (what user paid)
        total_spending = Decimal("0")
        monthly_spending = defaultdict(Decimal)
        quarterly_spending = defaultdict(Decimal)
        yearly_spending = defaultdict(Decimal)
        
        currency_code = "USD"  # Default, will be normalized
        
        for expense in valid_expenses:
            # Find user's participation
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                # Amount user paid (not owed)
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                total_spending += paid_share
                currency_code = expense.currency_code
                
                # Categorize by time period
                date = expense.date
                month_key = date.strftime("%Y-%m")
                quarter = (date.month - 1) // 3 + 1
                quarter_key = f"{date.year}-Q{quarter}"
                year_key = str(date.year)
                
                monthly_spending[month_key] += paid_share
                quarterly_spending[quarter_key] += paid_share
                yearly_spending[year_key] += paid_share
        
        # Convert to regular dicts
        monthly_dict = {k: v for k, v in sorted(monthly_spending.items())}
        quarterly_dict = {k: v for k, v in sorted(quarterly_spending.items())}
        yearly_dict = {k: v for k, v in sorted(yearly_spending.items())}
        
        # Calculate peak month and amount
        peak_month = None
        peak_amount = None
        if monthly_dict:
            peak_month = max(monthly_dict, key=monthly_dict.get)
            peak_amount = monthly_dict[peak_month]
        
        # Calculate monthly average
        monthly_average = None
        if monthly_dict:
            monthly_average = total_spending / len(monthly_dict)
        
        # Calculate spending trend (compare first half to second half of data)
        spending_trend = "stable"
        if len(monthly_dict) >= 4:
            sorted_months = sorted(monthly_dict.keys())
            mid = len(sorted_months) // 2
            first_half = sum(monthly_dict[m] for m in sorted_months[:mid])
            second_half = sum(monthly_dict[m] for m in sorted_months[mid:])
            
            # Compare averages
            first_avg = first_half / mid
            second_avg = second_half / (len(sorted_months) - mid)
            
            if second_avg > first_avg * Decimal("1.1"):  # 10% increase
                spending_trend = "increasing"
            elif second_avg < first_avg * Decimal("0.9"):  # 10% decrease
                spending_trend = "decreasing"
        
        # Generate explanation
        if yearly_dict:
            latest_year = max(yearly_dict.keys())
            latest_year_spending = yearly_dict[latest_year]
            explanation = (
                f"Total spending: {total_spending:,.2f} {currency_code}. "
                f"Latest year ({latest_year}) spending: {latest_year_spending:,.2f} {currency_code}. "
                f"Data spans {len(monthly_dict)} months across {len(yearly_dict)} years."
            )
        else:
            explanation = "No spending data available."
        
        return SpendingInsight(
            total_spending=total_spending,
            currency_code=currency_code,
            monthly_breakdown=monthly_dict,
            quarterly_breakdown=quarterly_dict,
            yearly_breakdown=yearly_dict,
            monthly_average=monthly_average,
            peak_month=peak_month,
            peak_amount=peak_amount,
            spending_trend=spending_trend,
            explanation=explanation
        )

