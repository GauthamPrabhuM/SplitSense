"""
Data normalizer for currency conversion and timestamp normalization.
"""
from typing import List, Dict, Any
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from models.schemas import Expense, Group, CurrencyCode


class DataNormalizer:
    """Normalize currencies and timestamps"""
    
    # Simple exchange rates (in production, use historical rates API)
    # Base currency: USD
    EXCHANGE_RATES = {
        "USD": Decimal("1.0"),
        "EUR": Decimal("1.10"),
        "GBP": Decimal("1.27"),
        "INR": Decimal("0.012"),
        "CAD": Decimal("0.74"),
        "AUD": Decimal("0.65"),
    }
    
    def __init__(self, base_currency: str = "USD"):
        """
        Initialize normalizer.
        
        Args:
            base_currency: Currency to normalize all amounts to
        """
        self.base_currency = base_currency.upper()
        if self.base_currency not in self.EXCHANGE_RATES:
            raise ValueError(f"Unsupported base currency: {base_currency}")
    
    def normalize_currency(self, amount: Decimal, from_currency: str) -> Decimal:
        """
        Convert amount from source currency to base currency.
        
        Args:
            amount: Amount in source currency
            from_currency: Source currency code
        
        Returns:
            Amount in base currency
        """
        from_currency = from_currency.upper()
        
        if from_currency == self.base_currency:
            return amount
        
        # Get exchange rate
        if from_currency not in self.EXCHANGE_RATES:
            # Unknown currency - assume 1:1 (should log warning in production)
            return amount
        
        # Convert: amount_in_base = amount_in_source * (base_rate / source_rate)
        source_rate = self.EXCHANGE_RATES[from_currency]
        base_rate = self.EXCHANGE_RATES[self.base_currency]
        
        converted = amount * (base_rate / source_rate)
        return converted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def normalize_timestamp(self, dt: datetime) -> datetime:
        """
        Normalize timestamp to UTC.
        
        Args:
            dt: Datetime object (may be timezone-aware or naive)
        
        Returns:
            UTC datetime
        """
        if dt.tzinfo is None:
            # Assume UTC if naive
            return dt.replace(tzinfo=timezone.utc)
        else:
            return dt.astimezone(timezone.utc)
    
    def normalize_expense(self, expense: Expense) -> Expense:
        """
        Normalize a single expense.
        
        Args:
            expense: Expense to normalize
        
        Returns:
            New Expense with normalized currency and timestamp
        """
        # Normalize cost
        normalized_cost = self.normalize_currency(expense.cost, expense.currency_code)
        
        # Normalize date
        normalized_date = self.normalize_timestamp(expense.date)
        
        # Normalize repayments
        normalized_repayments = []
        for repayment in expense.repayments:
            normalized_amount = self.normalize_currency(
                repayment.amount, repayment.currency_code
            )
            normalized_repayments.append(ExpenseRepayment(
                from_user=repayment.from_user,
                to_user=repayment.to_user,
                amount=normalized_amount,
                currency_code=self.base_currency
            ))
        
        # Create normalized expense
        normalized_expense = Expense(
            id=expense.id,
            group_id=expense.group_id,
            description=expense.description,
            payment=expense.payment,
            cost=normalized_cost,
            currency_code=self.base_currency,
            date=normalized_date,
            created_by=expense.created_by,
            users=expense.users,  # Users array may contain amounts that need normalization
            repayments=normalized_repayments,
            category=expense.category,
            receipt=expense.receipt,
            deleted_at=expense.deleted_at
        )
        
        # Normalize user amounts in users array
        normalized_users = []
        for user_data in expense.users:
            normalized_user_data = user_data.copy()
            
            # Normalize paid_share and owed_share if present
            if "paid_share" in normalized_user_data:
                paid_share = Decimal(str(normalized_user_data["paid_share"]))
                normalized_user_data["paid_share"] = str(
                    self.normalize_currency(paid_share, expense.currency_code)
                )
            
            if "owed_share" in normalized_user_data:
                owed_share = Decimal(str(normalized_user_data["owed_share"]))
                normalized_user_data["owed_share"] = str(
                    self.normalize_currency(owed_share, expense.currency_code)
                )
            
            normalized_users.append(normalized_user_data)
        
        normalized_expense.users = normalized_users
        
        return normalized_expense
    
    def normalize_expenses(self, expenses: List[Expense]) -> List[Expense]:
        """Normalize a list of expenses"""
        return [self.normalize_expense(exp) for exp in expenses]
    
    def normalize_groups(self, groups: List[Group]) -> List[Group]:
        """Normalize timestamps in groups"""
        normalized = []
        for group in groups:
            normalized_date = self.normalize_timestamp(group.updated_at)
            normalized_group = Group(
                id=group.id,
                name=group.name,
                group_type=group.group_type,
                updated_at=normalized_date,
                simplify_by_default=group.simplify_by_default,
                members=group.members
            )
            normalized.append(normalized_group)
        return normalized

