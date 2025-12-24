"""
Category analysis module.
Analyzes spending by category.
"""
from typing import Dict, List
from decimal import Decimal
from collections import defaultdict

from models.schemas import Expense, CategoryInsight


class CategoryAnalyzer:
    """Analyze spending by category"""
    
    def __init__(self, current_user_id: int):
        """
        Initialize analyzer.
        
        Args:
            current_user_id: ID of the current user
        """
        self.current_user_id = current_user_id
    
    def analyze(self, expenses: List[Expense]) -> CategoryInsight:
        """
        Analyze category-wise spending.
        
        Args:
            expenses: List of expenses
        
        Returns:
            CategoryInsight with category breakdowns
        """
        # Filter valid expenses
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        by_category = defaultdict(Decimal)
        currency_code = "USD"
        
        for expense in valid_expenses:
            category = expense.category or "Uncategorized"
            
            # Find user's participation
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                by_category[category] += paid_share
                currency_code = expense.currency_code
        
        # Calculate total for percentages
        total = sum(by_category.values())
        
        # Get top categories
        sorted_categories = sorted(
            by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        top_categories = []
        for category, amount in sorted_categories[:10]:  # Top 10
            percentage = (amount / total * 100) if total > 0 else 0
            top_categories.append({
                "category": category,
                "amount": float(amount),
                "percentage": round(float(percentage), 2)
            })
        
        # Generate explanation
        if top_categories:
            top_cat = top_categories[0]
            explanation = (
                f"Total spending across {len(by_category)} categories: "
                f"{total:,.2f} {currency_code}. "
                f"Top category: {top_cat['category']} ({top_cat['percentage']:.1f}%)."
            )
        else:
            explanation = "No category data available."
        
        return CategoryInsight(
            by_category=dict(by_category),
            currency_code=currency_code,
            top_categories=top_categories,
            explanation=explanation
        )

