"""
Balance analysis module.
Analyzes net balance trends and who owes whom.
"""
from typing import Dict, List
from decimal import Decimal
from collections import defaultdict
from datetime import datetime

from models.schemas import Expense, BalanceInsight


class BalanceAnalyzer:
    """Analyze balance trends"""
    
    def __init__(self, current_user_id: int):
        """
        Initialize analyzer.
        
        Args:
            current_user_id: ID of the current user
        """
        self.current_user_id = current_user_id
    
    def analyze(self, expenses: List[Expense]) -> BalanceInsight:
        """
        Analyze balance trends.
        
        Args:
            expenses: List of expenses
        
        Returns:
            BalanceInsight with balance breakdowns
        """
        # Filter valid expenses
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        # Calculate balances
        net_balance = Decimal("0")
        owed_to_user = Decimal("0")
        user_owes = Decimal("0")
        by_person = defaultdict(Decimal)
        trend_over_time = defaultdict(Decimal)
        
        currency_code = "USD"
        
        for expense in valid_expenses:
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                currency_code = expense.currency_code
                
                # Balance = paid - owed
                balance_change = paid_share - owed_share
                net_balance += balance_change
                
                # Track by person (simplified - would need to track all users in expense)
                # For now, we'll track net per expense
                if balance_change > 0:
                    owed_to_user += balance_change
                else:
                    user_owes += abs(balance_change)
                
                # Track trend over time
                month_key = expense.date.strftime("%Y-%m")
                trend_over_time[month_key] += balance_change
        
        # Calculate cumulative trend
        sorted_months = sorted(trend_over_time.keys())
        cumulative = Decimal("0")
        cumulative_trend = {}
        for month in sorted_months:
            cumulative += trend_over_time[month]
            cumulative_trend[month] = cumulative
        
        # Generate explanation
        if net_balance > 0:
            balance_desc = f"you are owed {net_balance:,.2f} {currency_code} net"
        elif net_balance < 0:
            balance_desc = f"you owe {abs(net_balance):,.2f} {currency_code} net"
        else:
            balance_desc = "your balances are settled"
        
        explanation = (
            f"Net balance: {net_balance:,.2f} {currency_code}. "
            f"Overall, {balance_desc}. "
            f"You are owed {owed_to_user:,.2f} {currency_code} and owe {user_owes:,.2f} {currency_code}."
        )
        
        return BalanceInsight(
            net_balance=net_balance,
            currency_code=currency_code,
            owed_to_user=owed_to_user,
            user_owes=user_owes,
            by_person=dict(by_person),
            trend_over_time=cumulative_trend,
            explanation=explanation
        )

