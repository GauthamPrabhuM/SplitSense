"""
Unit tests for analytics modules.
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from models.schemas import Expense, User, Group
from analytics import (
    SpendingAnalyzer,
    BalanceAnalyzer,
    CategoryAnalyzer,
    GroupAnalyzer,
)


@pytest.fixture
def sample_user():
    """Create a sample user"""
    return User(id=1, first_name="Test", last_name="User")


@pytest.fixture
def sample_expenses(sample_user):
    """Create sample expenses for testing"""
    expenses = []
    
    # Expense 1: Food, user paid $50, owes $25
    expenses.append(Expense(
        id=1,
        group_id=1,
        description="Dinner",
        payment=False,
        cost=Decimal("50.00"),
        currency_code="USD",
        date=datetime.now() - timedelta(days=10),
        created_by=sample_user,
        users=[
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
        repayments=[],
        category="Food & Drink"
    ))
    
    # Expense 2: Travel, user paid $100, owes $50
    expenses.append(Expense(
        id=2,
        group_id=1,
        description="Gas",
        payment=False,
        cost=Decimal("100.00"),
        currency_code="USD",
        date=datetime.now() - timedelta(days=5),
        created_by=sample_user,
        users=[
            {
                "user": {"id": 1, "first_name": "Test"},
                "paid_share": "100.00",
                "owed_share": "50.00"
            },
            {
                "user": {"id": 2, "first_name": "Friend"},
                "paid_share": "0.00",
                "owed_share": "50.00"
            }
        ],
        repayments=[],
        category="Travel"
    ))
    
    return expenses


@pytest.fixture
def sample_groups():
    """Create sample groups"""
    return [
        Group(
            id=1,
            name="Test Group",
            group_type="other",
            updated_at=datetime.now(),
            simplify_by_default=False,
            members=[]
        )
    ]


def test_spending_analyzer(sample_expenses):
    """Test spending analysis"""
    analyzer = SpendingAnalyzer(current_user_id=1)
    insight = analyzer.analyze(sample_expenses)
    
    # User paid $50 + $100 = $150
    assert insight.total_spending == Decimal("150.00")
    assert insight.currency_code == "USD"
    assert len(insight.monthly_breakdown) > 0


def test_balance_analyzer(sample_expenses):
    """Test balance analysis"""
    analyzer = BalanceAnalyzer(current_user_id=1)
    insight = analyzer.analyze(sample_expenses)
    
    # Net balance = (50-25) + (100-50) = 25 + 50 = 75
    assert insight.net_balance == Decimal("75.00")
    assert insight.owed_to_user == Decimal("75.00")
    assert insight.user_owes == Decimal("0.00")


def test_category_analyzer(sample_expenses):
    """Test category analysis"""
    analyzer = CategoryAnalyzer(current_user_id=1)
    insight = analyzer.analyze(sample_expenses)
    
    assert "Food & Drink" in insight.by_category
    assert "Travel" in insight.by_category
    assert insight.by_category["Food & Drink"] == Decimal("50.00")
    assert insight.by_category["Travel"] == Decimal("100.00")
    assert len(insight.top_categories) >= 2


def test_group_analyzer(sample_expenses, sample_groups):
    """Test group analysis"""
    analyzer = GroupAnalyzer(current_user_id=1)
    insight = analyzer.analyze(sample_expenses, sample_groups)
    
    assert 1 in insight.by_group
    assert insight.by_group[1]["total_spending"] == 150.0
    assert len(insight.top_groups) > 0


def test_spending_aggregation_correctness(sample_expenses):
    """Test that spending aggregation is mathematically correct"""
    analyzer = SpendingAnalyzer(current_user_id=1)
    insight = analyzer.analyze(sample_expenses)
    
    # Sum of monthly breakdown should equal total spending
    monthly_sum = sum(insight.monthly_breakdown.values())
    assert abs(monthly_sum - insight.total_spending) < Decimal("0.01")


def test_balance_calculation_correctness(sample_expenses):
    """Test that balance calculation is mathematically correct"""
    analyzer = BalanceAnalyzer(current_user_id=1)
    insight = analyzer.analyze(sample_expenses)
    
    # Net balance should equal owed_to_user - user_owes
    calculated_net = insight.owed_to_user - insight.user_owes
    assert abs(calculated_net - insight.net_balance) < Decimal("0.01")

