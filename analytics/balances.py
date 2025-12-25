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
        # Separate expenses and settlements
        valid_expenses = [e for e in expenses if not e.deleted_at and not e.payment]
        settlements = [e for e in expenses if not e.deleted_at and e.payment]
        
        # Calculate balances
        net_balance = Decimal("0")
        owed_to_user = Decimal("0")
        user_owes = Decimal("0")
        by_person_id = defaultdict(Decimal)  # user_id -> net balance (positive = they owe you)
        trend_over_time = defaultdict(Decimal)
        
        currency_code = "USD"
        
        # Build user name lookup from all expenses
        user_name_lookup = {}
        for expense in expenses:
            if expense.deleted_at:
                continue
            for user_data in expense.users:
                user_info = user_data.get("user", {})
                user_id = user_info.get("id")
                if user_id and user_id not in user_name_lookup:
                    first_name = user_info.get("first_name", "")
                    last_name = user_info.get("last_name", "")
                    if last_name and last_name != "None":
                        full_name = f"{first_name} {last_name}".strip()
                    else:
                        full_name = first_name.strip()
                    if full_name:
                        user_name_lookup[user_id] = full_name
        
        # Process each expense using repayments
        # Repayments explicitly tell us: from_user owes to_user the amount
        for expense in valid_expenses:
            currency_code = expense.currency_code
            month_key = expense.date.strftime("%Y-%m")
            
            for repayment in expense.repayments:
                from_user = repayment.from_user
                to_user = repayment.to_user
                amount = repayment.amount
                
                if to_user == self.current_user_id:
                    # Someone owes ME money
                    by_person_id[from_user] += amount
                    net_balance += amount
                    owed_to_user += amount
                    trend_over_time[month_key] += amount
                elif from_user == self.current_user_id:
                    # I owe someone money
                    by_person_id[to_user] -= amount
                    net_balance -= amount
                    user_owes += amount
                    trend_over_time[month_key] -= amount
        
        # Process settlements (payments reduce debt)
        for settlement in settlements:
            month_key = settlement.date.strftime("%Y-%m")
            
            for repayment in settlement.repayments:
                from_user = repayment.from_user
                to_user = repayment.to_user
                amount = repayment.amount
                
                if from_user == self.current_user_id:
                    # I paid someone (reduces what I owe them)
                    by_person_id[to_user] += amount
                    net_balance += amount
                    trend_over_time[month_key] += amount
                elif to_user == self.current_user_id:
                    # Someone paid me (reduces what they owe me)
                    by_person_id[from_user] -= amount
                    net_balance -= amount
                    trend_over_time[month_key] -= amount
        
        # Convert by_person_id to by_person with names
        by_person = {}
        for user_id, balance in by_person_id.items():
            if balance != 0:  # Only include non-zero balances
                person_name = user_name_lookup.get(user_id, f"User {user_id}")
                by_person[person_name] = balance
        
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

