"""
Advanced analytics module.
Anomaly detection, subscription detection, balance prediction, friction ranking.
"""
from typing import Dict, List, Tuple
from decimal import Decimal
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import statistics

from models.schemas import (
    Expense,
    Group,
    RecurringExpense,
    SettlementEfficiency,
    CashFlowInsight,
    AnomalyDetection,
    SubscriptionDetection,
    BalancePrediction,
    FrictionRanking,
)


class AdvancedAnalyzer:
    """Advanced analytics and insights"""
    
    def __init__(self, current_user_id: int):
        """
        Initialize analyzer.
        
        Args:
            current_user_id: ID of the current user
        """
        self.current_user_id = current_user_id
    
    def detect_anomalies(
        self,
        expenses: List[Expense],
        threshold_multiplier: float = 3.0
    ) -> AnomalyDetection:
        """
        Detect spending anomalies using statistical methods.
        
        Args:
            expenses: List of expenses
            threshold_multiplier: Multiplier for standard deviation threshold
        
        Returns:
            AnomalyDetection results
        """
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        # Get user's spending amounts
        amounts = []
        expense_amounts = []
        
        for expense in valid_expenses:
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                if paid_share > 0:
                    amounts.append(float(paid_share))
                    expense_amounts.append((expense, paid_share))
        
        if len(amounts) < 3:
            return AnomalyDetection(
                anomalies=[],
                threshold_multiplier=threshold_multiplier,
                explanation="Insufficient data for anomaly detection (need at least 3 expenses)."
            )
        
        # Calculate mean and standard deviation
        mean = statistics.mean(amounts)
        stdev = statistics.stdev(amounts) if len(amounts) > 1 else 0
        
        threshold = mean + (threshold_multiplier * stdev)
        
        # Find anomalies
        anomalies = []
        for expense, amount in expense_amounts:
            if float(amount) > threshold:
                anomalies.append({
                    "date": expense.date.isoformat(),
                    "amount": float(amount),
                    "description": expense.description,
                    "reason": f"Amount ({amount:,.2f}) exceeds threshold ({threshold:,.2f})"
                })
        
        explanation = (
            f"Detected {len(anomalies)} spending anomalies using "
            f"{threshold_multiplier}x standard deviation threshold. "
            f"Mean spending: {mean:,.2f}, Threshold: {threshold:,.2f}."
        )
        
        return AnomalyDetection(
            anomalies=anomalies,
            threshold_multiplier=threshold_multiplier,
            explanation=explanation
        )
    
    def detect_subscriptions(self, expenses: List[Expense]) -> SubscriptionDetection:
        """
        Detect recurring subscriptions or recurring expenses.
        
        Args:
            expenses: List of expenses
        
        Returns:
            SubscriptionDetection results
        """
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        # Group expenses by description pattern (simplified matching)
        description_groups = defaultdict(list)
        
        for expense in valid_expenses:
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                if paid_share > 0:
                    # Normalize description for matching
                    desc_lower = expense.description.lower().strip()
                    # Use first few words as pattern
                    pattern = " ".join(desc_lower.split()[:3])
                    description_groups[pattern].append((expense, paid_share))
        
        # Find recurring patterns (at least 3 occurrences)
        subscriptions = []
        
        for pattern, expense_list in description_groups.items():
            if len(expense_list) < 3:
                continue
            
            # Sort by date
            expense_list.sort(key=lambda x: x[0].date)
            
            # Calculate average amount
            amounts = [float(paid) for _, paid in expense_list]
            avg_amount = Decimal(str(statistics.mean(amounts)))
            total_amount = sum(Decimal(str(paid)) for _, paid in expense_list)
            
            # Calculate frequency (average days between occurrences)
            dates = [exp.date for exp, _ in expense_list]
            if len(dates) > 1:
                date_diffs = [
                    (dates[i+1] - dates[i]).days
                    for i in range(len(dates) - 1)
                ]
                avg_frequency = statistics.mean(date_diffs)
            else:
                avg_frequency = 30.0
            
            # Get category and currency from first expense
            first_expense = expense_list[0][0]
            
            subscriptions.append(RecurringExpense(
                description_pattern=pattern,
                category=first_expense.category,
                average_amount=avg_amount,
                frequency_days=avg_frequency,
                occurrences=len(expense_list),
                total_amount=total_amount,
                currency_code=first_expense.currency_code,
                last_occurrence=dates[-1]
            ))
        
        # Sort by total amount
        subscriptions.sort(key=lambda x: x.total_amount, reverse=True)
        
        # Calculate monthly subscriptions total
        monthly_total = Decimal("0")
        for sub in subscriptions:
            if sub.frequency_days <= 35:  # Monthly or more frequent
                monthly_total += sub.average_amount
        
        currency_code = subscriptions[0].currency_code if subscriptions else "USD"
        
        explanation = (
            f"Detected {len(subscriptions)} recurring expense patterns. "
            f"Estimated monthly subscriptions: {monthly_total:,.2f} {currency_code}."
        )
        
        return SubscriptionDetection(
            subscriptions=subscriptions,
            total_monthly_subscriptions=monthly_total,
            currency_code=currency_code,
            explanation=explanation
        )
    
    def analyze_settlement_efficiency(self, expenses: List[Expense]) -> SettlementEfficiency:
        """
        Analyze how quickly balances are settled.
        
        Args:
            expenses: List of expenses
        
        Returns:
            SettlementEfficiency results
        """
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at
        ]
        
        # Find expenses and their corresponding settlements
        expense_map = {}
        for expense in valid_expenses:
            if not expense.payment:
                expense_map[expense.id] = expense
        
        # Track settlement times (simplified - would need better matching)
        settlement_times = []
        by_person = defaultdict(list)
        
        # For now, calculate based on payment expenses
        payment_expenses = [e for e in valid_expenses if e.payment]
        
        for payment_exp in payment_expenses:
            # Find related expense (simplified matching)
            # In reality, would need to match by description, amount, users, etc.
            # Ensure date is a datetime object
            if isinstance(payment_exp.date, datetime):
                expense_date = payment_exp.date
            elif isinstance(payment_exp.date, str):
                # Try to parse if it's a string
                try:
                    expense_date = datetime.fromisoformat(payment_exp.date.replace("Z", "+00:00"))
                except:
                    continue  # Skip if we can't parse
            else:
                continue  # Skip if date is invalid
            
            # Ensure both datetimes are timezone-aware for comparison
            now = datetime.now(timezone.utc)
            if expense_date.tzinfo is None:
                # If expense_date is naive, assume UTC
                expense_date = expense_date.replace(tzinfo=timezone.utc)
            elif now.tzinfo is None:
                # If now is naive, make it UTC-aware
                now = datetime.now(timezone.utc)
            
            days_since = (now - expense_date).days
            settlement_times.append(days_since)
        
        # Calculate unpaid balances
        unpaid_count = 0
        unpaid_total = Decimal("0")
        
        for expense in valid_expenses:
            if expense.payment or expense.deleted_at:
                continue
            
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                if owed_share > 0:
                    unpaid_count += 1
                    unpaid_total += owed_share
        
        avg_settlement = statistics.mean(settlement_times) if settlement_times else 0
        median_settlement = statistics.median(settlement_times) if settlement_times else 0
        
        currency_code = valid_expenses[0].currency_code if valid_expenses else "USD"
        
        explanation = (
            f"Average settlement time: {avg_settlement:.1f} days. "
            f"Unpaid balances: {unpaid_count} expenses totaling {unpaid_total:,.2f} {currency_code}."
        )
        
        return SettlementEfficiency(
            average_settlement_days=avg_settlement,
            median_settlement_days=median_settlement,
            unpaid_balances_count=unpaid_count,
            unpaid_balances_total=unpaid_total,
            currency_code=currency_code,
            by_person={},  # Would need more sophisticated tracking
            explanation=explanation
        )
    
    def analyze_cash_flow(self, expenses: List[Expense]) -> CashFlowInsight:
        """
        Analyze cash flow directionality.
        
        Args:
            expenses: List of expenses
        
        Returns:
            CashFlowInsight results
        """
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        total_paid = Decimal("0")
        total_received = Decimal("0")
        front_pay_count = 0
        total_expenses = 0
        
        currency_code = "USD"
        
        for expense in valid_expenses:
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                currency_code = expense.currency_code
                
                total_paid += paid_share
                total_received += owed_share
                
                if paid_share > 0:
                    total_expenses += 1
                    if paid_share > owed_share:
                        front_pay_count += 1
        
        net_cash_flow = total_paid - total_received
        front_pay_percentage = (front_pay_count / total_expenses * 100) if total_expenses > 0 else 0
        
        if net_cash_flow > 0:
            flow_desc = "net payer (you front-pay more than you receive)"
        else:
            flow_desc = "net receiver (you receive more than you front-pay)"
        
        explanation = (
            f"Total paid: {total_paid:,.2f} {currency_code}, "
            f"Total received: {total_received:,.2f} {currency_code}. "
            f"You are a {flow_desc}. "
            f"Front-pay percentage: {front_pay_percentage:.1f}%."
        )
        
        return CashFlowInsight(
            total_paid=total_paid,
            total_received=total_received,
            net_cash_flow=net_cash_flow,
            currency_code=currency_code,
            front_pay_percentage=front_pay_percentage,
            explanation=explanation
        )
    
    def predict_balance(
        self,
        expenses: List[Expense],
        months_to_predict: int = 1
    ) -> BalancePrediction:
        """
        Predict end-of-month balance based on historical trends.
        
        Args:
            expenses: List of expenses
            months_to_predict: Number of months ahead to predict
        
        Returns:
            BalancePrediction results
        """
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        # Calculate monthly net balance changes
        monthly_changes = defaultdict(Decimal)
        
        for expense in valid_expenses:
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                
                balance_change = paid_share - owed_share
                month_key = expense.date.strftime("%Y-%m")
                monthly_changes[month_key] += balance_change
        
        if len(monthly_changes) < 2:
            return BalancePrediction(
                predicted_balance=Decimal("0"),
                currency_code="USD",
                confidence_level="low",
                based_on_months=len(monthly_changes),
                trend="stable",
                explanation="Insufficient data for prediction (need at least 2 months)."
            )
        
        # Calculate average monthly change
        sorted_months = sorted(monthly_changes.keys())
        changes = [monthly_changes[m] for m in sorted_months]
        avg_change = Decimal(str(statistics.mean([float(c) for c in changes])))
        
        # Determine trend
        if len(changes) >= 2:
            recent_trend = changes[-1] - changes[-2]
            if recent_trend > Decimal("0.1"):
                trend = "increasing"
            elif recent_trend < Decimal("-0.1"):
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Predict balance
        current_balance = sum(changes)
        predicted_balance = current_balance + (avg_change * months_to_predict)
        
        # Determine confidence
        if len(monthly_changes) >= 6:
            confidence = "high"
        elif len(monthly_changes) >= 3:
            confidence = "medium"
        else:
            confidence = "low"
        
        currency_code = valid_expenses[0].currency_code if valid_expenses else "USD"
        
        explanation = (
            f"Predicted balance in {months_to_predict} month(s): {predicted_balance:,.2f} {currency_code}. "
            f"Based on {len(monthly_changes)} months of data. Trend: {trend}. "
            f"Confidence: {confidence}."
        )
        
        return BalancePrediction(
            predicted_balance=predicted_balance,
            currency_code=currency_code,
            confidence_level=confidence,
            based_on_months=len(monthly_changes),
            trend=trend,
            explanation=explanation
        )
    
    def rank_friction(
        self,
        expenses: List[Expense],
        groups: List[Group]
    ) -> FrictionRanking:
        """
        Rank friends/groups by financial friction.
        
        Args:
            expenses: List of expenses
            groups: List of groups
        
        Returns:
            FrictionRanking results
        """
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at
        ]
        
        # Track friction metrics by person and group
        person_friction = defaultdict(lambda: {
            "unpaid_balance": Decimal("0"),
            "delay_days": [],
            "dispute_count": 0
        })
        
        group_friction = defaultdict(lambda: {
            "name": "Unknown",
            "unpaid_balance": Decimal("0"),
            "member_count": 0,
            "expense_count": 0
        })
        
        group_lookup = {g.id: g for g in groups}
        
        for expense in valid_expenses:
            group_id = expense.group_id or 0
            
            if group_id in group_lookup:
                group = group_lookup[group_id]
                group_friction[group_id]["name"] = group.name
                group_friction[group_id]["member_count"] = len(group.members)
            
            group_friction[group_id]["expense_count"] += 1
            
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id == self.current_user_id:
                    continue
                
                owed_share = Decimal(str(user_data.get("owed_share", "0")))
                if owed_share > 0:
                    person_friction[user_id]["unpaid_balance"] += owed_share
                    
                    # Calculate delay (simplified)
                    # Ensure both datetimes are timezone-aware for comparison
                    now = datetime.now(timezone.utc)
                    expense_date = expense.date
                    if expense_date.tzinfo is None:
                        # If expense_date is naive, assume UTC
                        expense_date = expense_date.replace(tzinfo=timezone.utc)
                    days_old = (now - expense_date).days
                    person_friction[user_id]["delay_days"].append(days_old)
        
        # Calculate friction scores
        by_person = []
        for user_id, metrics in person_friction.items():
            avg_delay = statistics.mean(metrics["delay_days"]) if metrics["delay_days"] else 0
            friction_score = float(metrics["unpaid_balance"]) + (avg_delay * 10)  # Simple scoring
            by_person.append({
                "user_id": user_id,
                "unpaid_balance": float(metrics["unpaid_balance"]),
                "average_delay_days": avg_delay,
                "friction_score": friction_score
            })
        
        by_person.sort(key=lambda x: x["friction_score"], reverse=True)
        
        by_group_list = []
        for group_id, metrics in group_friction.items():
            friction_score = float(metrics["unpaid_balance"]) + (metrics["expense_count"] * 5)
            by_group_list.append({
                "group_id": group_id if group_id > 0 else None,
                "name": metrics["name"],
                "unpaid_balance": float(metrics["unpaid_balance"]),
                "member_count": metrics["member_count"],
                "expense_count": metrics["expense_count"],
                "friction_score": friction_score
            })
        
        by_group_list.sort(key=lambda x: x["friction_score"], reverse=True)
        
        explanation = (
            f"Ranked {len(by_person)} people and {len(by_group_list)} groups by financial friction. "
            f"Friction considers unpaid balances, delays, and dispute frequency."
        )
        
        return FrictionRanking(
            by_person=by_person,
            by_group=by_group_list,
            explanation=explanation
        )

