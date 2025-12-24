"""
Data models for Splitwise Analysis Tool.
All models use Pydantic for validation and type safety.
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class CurrencyCode(str, Enum):
    """Supported currency codes"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"
    CAD = "CAD"
    AUD = "AUD"
    # Add more as needed


class User(BaseModel):
    """Splitwise user model"""
    id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    picture: Optional[str] = None


class Group(BaseModel):
    """Splitwise group model"""
    id: int
    name: str
    group_type: str  # 'household', 'trip', 'other', etc.
    updated_at: datetime
    simplify_by_default: bool = False
    members: List[User] = []


class ExpenseRepayment(BaseModel):
    """Repayment details for an expense"""
    from_user: int
    to_user: int
    amount: Decimal
    currency_code: str


class Expense(BaseModel):
    """Splitwise expense model"""
    id: int
    group_id: Optional[int] = None
    description: str
    payment: bool = False  # True if this is a payment/settlement
    cost: Decimal
    currency_code: str
    date: datetime
    created_by: User
    users: List[Dict[str, Any]]  # List of user participation details
    repayments: List[ExpenseRepayment] = []
    category: Optional[str] = None
    receipt: Optional[str] = None
    deleted_at: Optional[datetime] = None

    @field_validator('cost')
    @classmethod
    def validate_cost(cls, v):
        if v < 0:
            raise ValueError("Cost cannot be negative")
        return v


class Debt(BaseModel):
    """Debt relationship between users"""
    from_user: int
    to_user: int
    amount: Decimal
    currency_code: str


class Balance(BaseModel):
    """Balance information for a user in a group"""
    user_id: int
    group_id: Optional[int] = None
    amount: Decimal  # Positive = owed to user, Negative = user owes
    currency_code: str


# Data container models
class ExpenseData(BaseModel):
    """Container for all expense data"""
    expenses: List[Expense] = []
    raw_count: int = 0
    filtered_count: int = 0


class GroupData(BaseModel):
    """Container for all group data"""
    groups: List[Group] = []
    raw_count: int = 0


class UserData(BaseModel):
    """Container for all user data"""
    users: Dict[int, User] = {}  # user_id -> User
    current_user_id: Optional[int] = None


# Validation models
class ValidationResult(BaseModel):
    """Result of data integrity validation"""
    is_valid: bool
    checks: List[Dict[str, Any]] = []
    errors: List[str] = []
    warnings: List[str] = []


# Analytics insight models
class SpendingInsight(BaseModel):
    """Spending trends over time"""
    total_spending: Decimal
    currency_code: str
    monthly_breakdown: Dict[str, Decimal]  # "YYYY-MM" -> amount
    quarterly_breakdown: Dict[str, Decimal]  # "YYYY-Q1" -> amount
    yearly_breakdown: Dict[str, Decimal]  # "YYYY" -> amount
    explanation: str


class BalanceInsight(BaseModel):
    """Net balance trends"""
    net_balance: Decimal  # Positive = net owed to user, Negative = user owes net
    currency_code: str
    owed_to_user: Decimal
    user_owes: Decimal
    by_person: Dict[int, Decimal]  # user_id -> net balance
    trend_over_time: Dict[str, Decimal]  # "YYYY-MM" -> net balance
    explanation: str


class CategoryInsight(BaseModel):
    """Category-wise spending breakdown"""
    by_category: Dict[str, Decimal]  # category -> total amount
    currency_code: str
    top_categories: List[Dict[str, Any]]  # [{"category": str, "amount": Decimal, "percentage": float}]
    explanation: str


class GroupInsight(BaseModel):
    """Group-wise spending breakdown"""
    by_group: Dict[int, Dict[str, Any]]  # group_id -> {name, total_spending, member_count}
    currency_code: str
    top_groups: List[Dict[str, Any]]
    explanation: str


class RecurringExpense(BaseModel):
    """Recurring expense pattern"""
    description_pattern: str
    category: Optional[str]
    average_amount: Decimal
    frequency_days: float
    occurrences: int
    total_amount: Decimal
    currency_code: str
    last_occurrence: datetime


class SettlementEfficiency(BaseModel):
    """Settlement efficiency metrics"""
    average_settlement_days: float
    median_settlement_days: float
    unpaid_balances_count: int
    unpaid_balances_total: Decimal
    currency_code: str
    by_person: Dict[int, float]  # user_id -> average settlement days
    explanation: str


class CashFlowInsight(BaseModel):
    """Cash flow directionality analysis"""
    total_paid: Decimal
    total_received: Decimal
    net_cash_flow: Decimal  # Positive = net payer, Negative = net receiver
    currency_code: str
    front_pay_percentage: float  # Percentage of expenses user front-paid
    explanation: str


class AnomalyDetection(BaseModel):
    """Spending anomaly detection results"""
    anomalies: List[Dict[str, Any]]  # [{"date": datetime, "amount": Decimal, "reason": str}]
    threshold_multiplier: float
    explanation: str


class SubscriptionDetection(BaseModel):
    """Detected recurring subscriptions"""
    subscriptions: List[RecurringExpense]
    total_monthly_subscriptions: Decimal
    currency_code: str
    explanation: str


class BalancePrediction(BaseModel):
    """Predicted end-of-month balance"""
    predicted_balance: Decimal
    currency_code: str
    confidence_level: str  # "high", "medium", "low"
    based_on_months: int
    trend: str  # "increasing", "decreasing", "stable"
    explanation: str


class FrictionRanking(BaseModel):
    """Financial friction ranking for friends/groups"""
    by_person: List[Dict[str, Any]]  # Ranked by friction score
    by_group: List[Dict[str, Any]]  # Ranked by friction score
    explanation: str


class AllInsights(BaseModel):
    """Container for all generated insights"""
    validation: ValidationResult
    spending: SpendingInsight
    balance: BalanceInsight
    categories: CategoryInsight
    groups: GroupInsight
    recurring: List[RecurringExpense]
    settlement_efficiency: SettlementEfficiency
    cash_flow: CashFlowInsight
    anomalies: AnomalyDetection
    subscriptions: SubscriptionDetection
    balance_prediction: BalancePrediction
    friction: FrictionRanking
    generated_at: datetime = Field(default_factory=datetime.now)
    data_summary: Dict[str, Any]  # Summary of ingested data

