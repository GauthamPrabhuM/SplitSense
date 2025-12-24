"""
Data integrity verification module.
Cross-verifies totals, balances, and consistency.
"""
from typing import List, Dict, Any
from decimal import Decimal
from collections import defaultdict

from models.schemas import Expense, Group, Balance, ValidationResult, UserData


class DataVerifier:
    """Verify data integrity and consistency"""
    
    def __init__(self, current_user_id: int):
        """
        Initialize verifier.
        
        Args:
            current_user_id: ID of the current user (for balance calculations)
        """
        self.current_user_id = current_user_id
    
    def verify_expense_totals(self, expenses: List[Expense]) -> List[Dict[str, Any]]:
        """
        Verify that for each expense, sum of paid shares equals sum of owed shares.
        
        Returns:
            List of check results
        """
        checks = []
        errors = []
        
        for expense in expenses:
            if expense.deleted_at:
                continue
            
            total_paid = Decimal("0")
            total_owed = Decimal("0")
            
            for user_data in expense.users:
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                
                total_paid += paid_share
                total_owed += owed_share
            
            # Allow small rounding differences (0.01)
            difference = abs(total_paid - total_owed)
            if difference > Decimal("0.01"):
                errors.append(
                    f"Expense {expense.id} ({expense.description}): "
                    f"Paid total ({total_paid}) != Owed total ({total_owed}), "
                    f"difference: {difference}"
                )
            
            checks.append({
                "type": "expense_totals",
                "expense_id": expense.id,
                "total_paid": float(total_paid),
                "total_owed": float(total_owed),
                "difference": float(difference),
                "is_valid": difference <= Decimal("0.01")
            })
        
        return checks, errors
    
    def verify_group_balances(self, expenses: List[Expense], groups: List[Group]) -> List[Dict[str, Any]]:
        """
        Verify that sum of all balances in each group equals zero.
        
        Returns:
            List of check results
        """
        checks = []
        errors = []
        
        # Calculate balances per group
        group_balances = defaultdict(lambda: defaultdict(Decimal))  # group_id -> user_id -> balance
        
        for expense in expenses:
            if expense.deleted_at or expense.payment:
                continue
            
            group_id = expense.group_id or 0  # 0 for no group
            
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if not user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                
                # Balance = paid - owed (positive = user is owed, negative = user owes)
                balance_change = paid_share - owed_share
                group_balances[group_id][user_id] += balance_change
        
        # Verify each group sums to zero
        for group_id, user_balances in group_balances.items():
            total_balance = sum(user_balances.values())
            
            # Allow small rounding differences
            if abs(total_balance) > Decimal("0.01"):
                group_name = next(
                    (g.name for g in groups if g.id == group_id),
                    f"Group {group_id}" if group_id > 0 else "No Group"
                )
                errors.append(
                    f"{group_name}: Total balance ({total_balance}) != 0"
                )
            
            checks.append({
                "type": "group_balance",
                "group_id": group_id if group_id > 0 else None,
                "total_balance": float(total_balance),
                "user_count": len(user_balances),
                "is_valid": abs(total_balance) <= Decimal("0.01")
            })
        
        return checks, errors
    
    def verify_settlements(self, expenses: List[Expense]) -> List[Dict[str, Any]]:
        """
        Verify that settlement transactions balance to zero.
        
        Returns:
            List of check results
        """
        checks = []
        errors = []
        
        settlement_expenses = [e for e in expenses if e.payment]
        
        for expense in settlement_expenses:
            if expense.deleted_at:
                continue
            
            # For settlements, sum of repayments should equal the cost
            repayment_total = sum(r.amount for r in expense.repayments)
            difference = abs(expense.cost - repayment_total)
            
            if difference > Decimal("0.01"):
                errors.append(
                    f"Settlement expense {expense.id}: "
                    f"Cost ({expense.cost}) != Repayment total ({repayment_total})"
                )
            
            checks.append({
                "type": "settlement",
                "expense_id": expense.id,
                "cost": float(expense.cost),
                "repayment_total": float(repayment_total),
                "difference": float(difference),
                "is_valid": difference <= Decimal("0.01")
            })
        
        return checks, errors
    
    def verify_currency_consistency(self, expenses: List[Expense], groups: List[Group]) -> List[Dict[str, Any]]:
        """
        Check currency consistency within groups.
        
        Returns:
            List of check results
        """
        checks = []
        warnings = []
        
        # Group expenses by group_id
        group_expenses = defaultdict(list)
        for expense in expenses:
            if expense.deleted_at:
                continue
            group_id = expense.group_id or 0
            group_expenses[group_id].append(expense)
        
        for group_id, group_exp_list in group_expenses.items():
            currencies = set(exp.currency_code for exp in group_exp_list)
            
            if len(currencies) > 1:
                group_name = next(
                    (g.name for g in groups if g.id == group_id),
                    f"Group {group_id}" if group_id > 0 else "No Group"
                )
                warnings.append(
                    f"{group_name}: Multiple currencies detected: {', '.join(currencies)}. "
                    f"Ensure proper normalization."
                )
            
            checks.append({
                "type": "currency_consistency",
                "group_id": group_id if group_id > 0 else None,
                "currencies": list(currencies),
                "currency_count": len(currencies),
                "is_valid": len(currencies) <= 1
            })
        
        return checks, warnings
    
    def calculate_net_balance(self, expenses: List[Expense]) -> Decimal:
        """
        Calculate net balance for current user.
        
        Returns:
            Net balance (positive = owed to user, negative = user owes)
        """
        net_balance = Decimal("0")
        
        for expense in expenses:
            if expense.deleted_at:
                continue
            
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                
                # Balance = paid - owed
                net_balance += (paid_share - owed_share)
        
        return net_balance
    
    def verify_net_balance(self, expenses: List[Expense]) -> List[Dict[str, Any]]:
        """
        Verify net balance calculation consistency.
        
        Returns:
            Check results
        """
        checks = []
        
        # Calculate net balance from expenses
        calculated_balance = self.calculate_net_balance(expenses)
        
        # Also calculate from repayments in settlements
        settlement_balance = Decimal("0")
        for expense in expenses:
            if expense.deleted_at or not expense.payment:
                continue
            
            for repayment in expense.repayments:
                if repayment.from_user == self.current_user_id:
                    settlement_balance -= repayment.amount
                elif repayment.to_user == self.current_user_id:
                    settlement_balance += repayment.amount
        
        # Net balance should account for settlements
        total_balance = calculated_balance + settlement_balance
        
        checks.append({
            "type": "net_balance",
            "calculated_from_expenses": float(calculated_balance),
            "settlement_adjustment": float(settlement_balance),
            "total_net_balance": float(total_balance),
            "is_valid": True  # This is informational
        })
        
        return checks, []
    
    def verify_all(
        self,
        expenses: List[Expense],
        groups: List[Group]
    ) -> ValidationResult:
        """
        Run all verification checks.
        
        Returns:
            ValidationResult with all checks and issues
        """
        all_checks = []
        all_errors = []
        all_warnings = []
        
        # Run all checks
        checks, errors = self.verify_expense_totals(expenses)
        all_checks.extend(checks)
        all_errors.extend(errors)
        
        checks, errors = self.verify_group_balances(expenses, groups)
        all_checks.extend(checks)
        all_errors.extend(errors)
        
        checks, errors = self.verify_settlements(expenses)
        all_checks.extend(checks)
        all_errors.extend(errors)
        
        checks, warnings = self.verify_currency_consistency(expenses, groups)
        all_checks.extend(checks)
        all_warnings.extend(warnings)
        
        checks, errors = self.verify_net_balance(expenses)
        all_checks.extend(checks)
        all_errors.extend(errors)
        
        # Determine overall validity
        is_valid = len(all_errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            checks=all_checks,
            errors=all_errors,
            warnings=all_warnings
        )

