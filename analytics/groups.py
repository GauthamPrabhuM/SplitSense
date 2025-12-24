"""
Group analysis module.
Analyzes spending by group.
"""
from typing import Dict, List
from decimal import Decimal
from collections import defaultdict

from models.schemas import Expense, Group, GroupInsight


class GroupAnalyzer:
    """Analyze spending by group"""
    
    def __init__(self, current_user_id: int):
        """
        Initialize analyzer.
        
        Args:
            current_user_id: ID of the current user
        """
        self.current_user_id = current_user_id
    
    def analyze(self, expenses: List[Expense], groups: List[Group]) -> GroupInsight:
        """
        Analyze group-wise spending.
        
        Args:
            expenses: List of expenses
            groups: List of groups
        
        Returns:
            GroupInsight with group breakdowns
        """
        # Filter valid expenses
        valid_expenses = [
            e for e in expenses
            if not e.deleted_at and not e.payment
        ]
        
        # Create group lookup
        group_lookup = {g.id: g for g in groups}
        
        by_group = defaultdict(lambda: {
            "name": "Unknown",
            "total_spending": Decimal("0"),
            "member_count": 0,
            "expense_count": 0
        })
        
        currency_code = "USD"
        
        for expense in valid_expenses:
            group_id = expense.group_id or 0
            
            # Get group info
            if group_id in group_lookup:
                group = group_lookup[group_id]
                group_name = group.name
                member_count = len(group.members)
            else:
                group_name = "No Group" if group_id == 0 else f"Group {group_id}"
                member_count = 0
            
            # Find user's participation
            for user_data in expense.users:
                user_id = user_data.get("user", {}).get("id")
                if user_id != self.current_user_id:
                    continue
                
                paid_share = Decimal(str(user_data.get("paid_share", "0")))
                by_group[group_id]["name"] = group_name
                by_group[group_id]["total_spending"] += paid_share
                by_group[group_id]["member_count"] = member_count
                by_group[group_id]["expense_count"] += 1
                currency_code = expense.currency_code
        
        # Convert to proper format
        by_group_dict = {}
        for group_id, data in by_group.items():
            by_group_dict[group_id] = {
                "name": data["name"],
                "total_spending": float(data["total_spending"]),
                "member_count": data["member_count"],
                "expense_count": data["expense_count"]
            }
        
        # Get top groups
        sorted_groups = sorted(
            by_group_dict.items(),
            key=lambda x: x[1]["total_spending"],
            reverse=True
        )
        
        top_groups = []
        for group_id, data in sorted_groups[:10]:  # Top 10
            top_groups.append({
                "group_id": group_id if group_id > 0 else None,
                "name": data["name"],
                "total_spending": data["total_spending"],
                "member_count": data["member_count"],
                "expense_count": data["expense_count"]
            })
        
        # Generate explanation
        if top_groups:
            top_group = top_groups[0]
            explanation = (
                f"Spending across {len(by_group_dict)} groups: "
                f"{sum(d['total_spending'] for d in by_group_dict.values()):,.2f} {currency_code}. "
                f"Top group: {top_group['name']} ({top_group['total_spending']:,.2f} {currency_code})."
            )
        else:
            explanation = "No group data available."
        
        return GroupInsight(
            by_group=by_group_dict,
            currency_code=currency_code,
            top_groups=top_groups,
            explanation=explanation
        )

