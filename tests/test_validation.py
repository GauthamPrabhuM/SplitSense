"""
Unit tests for validation module.
"""
import pytest
from decimal import Decimal
from datetime import datetime

from models.schemas import Expense, User, Group
from validation import DataVerifier


@pytest.fixture
def sample_user():
    """Create a sample user"""
    return User(id=1, first_name="Test", last_name="User")


@pytest.fixture
def valid_expense(sample_user):
    """Create a valid expense (paid total = owed total)"""
    return Expense(
        id=1,
        group_id=1,
        description="Test Expense",
        payment=False,
        cost=Decimal("100.00"),
        currency_code="USD",
        date=datetime.now(),
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
        category="Test"
    )


@pytest.fixture
def invalid_expense(sample_user):
    """Create an invalid expense (paid total != owed total)"""
    return Expense(
        id=2,
        group_id=1,
        description="Invalid Expense",
        payment=False,
        cost=Decimal("100.00"),
        currency_code="USD",
        date=datetime.now(),
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
                "owed_share": "40.00"  # Should be 50.00
            }
        ],
        repayments=[],
        category="Test"
    )


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


def test_expense_totals_validation_valid(valid_expense):
    """Test validation of valid expense totals"""
    verifier = DataVerifier(current_user_id=1)
    checks, errors = verifier.verify_expense_totals([valid_expense])
    
    assert len(errors) == 0
    assert any(c["expense_id"] == 1 and c["is_valid"] for c in checks)


def test_expense_totals_validation_invalid(invalid_expense):
    """Test validation detects invalid expense totals"""
    verifier = DataVerifier(current_user_id=1)
    checks, errors = verifier.verify_expense_totals([invalid_expense])
    
    assert len(errors) > 0
    assert any("Expense 2" in error for error in errors)


def test_group_balance_validation(valid_expense, sample_groups):
    """Test group balance validation"""
    verifier = DataVerifier(current_user_id=1)
    checks, errors = verifier.verify_group_balances([valid_expense], sample_groups)
    
    # Group balance should sum to zero (user 1: +50, user 2: -50)
    group_check = next((c for c in checks if c["type"] == "group_balance"), None)
    assert group_check is not None
    assert abs(group_check["total_balance"]) < 0.01  # Should be ~0


def test_currency_consistency(valid_expense, sample_groups):
    """Test currency consistency check"""
    verifier = DataVerifier(current_user_id=1)
    checks, warnings = verifier.verify_currency_consistency([valid_expense], sample_groups)
    
    currency_check = next((c for c in checks if c["type"] == "currency_consistency"), None)
    assert currency_check is not None
    assert currency_check["currency_count"] == 1  # All same currency


def test_full_validation(valid_expense, sample_groups):
    """Test full validation process"""
    verifier = DataVerifier(current_user_id=1)
    result = verifier.verify_all([valid_expense], sample_groups)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.checks) > 0


def test_validation_with_invalid_data(invalid_expense, sample_groups):
    """Test validation with invalid data"""
    verifier = DataVerifier(current_user_id=1)
    result = verifier.verify_all([invalid_expense], sample_groups)
    
    # Should detect the error
    assert not result.is_valid or len(result.errors) > 0

