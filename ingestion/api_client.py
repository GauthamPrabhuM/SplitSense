"""
Splitwise REST API client with pagination and rate limit handling.
"""
import time
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

from models.schemas import Expense, User, Group, ExpenseRepayment


class SplitwiseAPIClient:
    """Client for Splitwise REST API"""
    
    BASE_URL = "https://secure.splitwise.com/api/v3.0"
    RATE_LIMIT_DELAY = 0.5  # Seconds between requests to respect rate limits
    
    def __init__(self, api_token: str):
        """
        Initialize API client.
        
        Args:
            api_token: Personal access token from Splitwise
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        })
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Ensure we respect rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request with rate limiting"""
        self._rate_limit()
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        
        # Check if response is successful
        if response.status_code != 200:
            error_text = response.text[:500]  # First 500 chars
            raise Exception(
                f"API request failed with status {response.status_code}. "
                f"Response: {error_text}"
            )
        
        # Check if response is JSON
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type:
            error_text = response.text[:500]
            raise Exception(
                f"API returned non-JSON response. Content-Type: {content_type}. "
                f"Response: {error_text}"
            )
        
        try:
            return response.json()
        except ValueError as e:
            error_text = response.text[:500]
            raise Exception(
                f"Failed to parse JSON response. Error: {str(e)}. "
                f"Response: {error_text}"
            )
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        data = self._get("get_current_user")
        return data.get("user", {})
    
    def get_groups(self) -> List[Dict[str, Any]]:
        """Get all groups"""
        data = self._get("get_groups")
        return data.get("groups", [])
    
    def get_expenses(
        self,
        group_id: Optional[int] = None,
        dated_after: Optional[str] = None,
        dated_before: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get expenses with pagination support.
        
        Args:
            group_id: Optional group ID to filter by
            dated_after: ISO date string (YYYY-MM-DD)
            dated_before: ISO date string (YYYY-MM-DD)
            limit: Number of expenses per page (max 100)
        
        Returns:
            List of all expenses (handles pagination automatically)
        """
        all_expenses = []
        offset = 0
        params = {"limit": min(limit, 100)}
        
        if group_id:
            params["group_id"] = group_id
        if dated_after:
            params["dated_after"] = dated_after
        if dated_before:
            params["dated_before"] = dated_before
        
        while True:
            params["offset"] = offset
            data = self._get("get_expenses", params=params)
            expenses = data.get("expenses", [])
            
            if not expenses:
                break
            
            all_expenses.extend(expenses)
            
            # Check if there are more pages
            if len(expenses) < params["limit"]:
                break
            
            offset += len(expenses)
        
        return all_expenses
    
    def get_friends(self) -> List[Dict[str, Any]]:
        """Get all friends"""
        data = self._get("get_friends")
        return data.get("friends", [])
    
    def parse_expense(self, expense_data: Dict[str, Any]) -> Expense:
        """Parse raw expense data into Expense model"""
        # Parse users
        users_data = expense_data.get("users", [])
        
        # Get expense currency - repayments use the same currency as the expense
        expense_currency = expense_data.get("currency_code", "USD")
        
        # Parse repayments
        repayments = []
        for repayment_data in expense_data.get("repayments", []):
            repayments.append(ExpenseRepayment(
                from_user=repayment_data["from"],
                to_user=repayment_data["to"],
                amount=Decimal(str(repayment_data["amount"])),
                currency_code=expense_currency  # Use expense currency, not default USD
            ))
        
        # Parse created_by user
        created_by_data = expense_data.get("created_by", {})
        user_id = created_by_data.get("id")
        if user_id is None:
            user_id = 0  # Default fallback for missing IDs
        created_by = User(
            id=user_id,
            first_name=created_by_data.get("first_name", "") or "",
            last_name=created_by_data.get("last_name", "") or "",
            email=created_by_data.get("email"),
            picture=created_by_data.get("picture", {}).get("medium") if created_by_data.get("picture") else None
        )
        
        # Parse date
        date_str = expense_data.get("date", "")
        if date_str:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            date = datetime.now()
        
        # Parse deleted_at
        deleted_at = None
        if expense_data.get("deleted_at"):
            deleted_at = datetime.fromisoformat(
                expense_data["deleted_at"].replace("Z", "+00:00")
            )
        
        # Ensure expense ID is valid
        expense_id = expense_data.get("id")
        if expense_id is None:
            raise ValueError("Expense missing required 'id' field")
        
        return Expense(
            id=expense_id,
            group_id=expense_data.get("group_id"),
            description=expense_data.get("description", ""),
            payment=expense_data.get("payment", False),
            cost=Decimal(str(expense_data.get("cost", 0))),
            currency_code=expense_data.get("currency_code", "USD"),
            date=date,
            created_by=created_by,
            users=users_data,
            repayments=repayments,
            category=expense_data.get("category", {}).get("name") if expense_data.get("category") else None,
            receipt=expense_data.get("receipt", {}).get("original") if expense_data.get("receipt") else None,
            deleted_at=deleted_at
        )
    
    def parse_group(self, group_data: Dict[str, Any]) -> Group:
        """Parse raw group data into Group model"""
        # Parse members
        members = []
        for member_data in group_data.get("members", []):
            user_data = member_data.get("user", {})
            user_id = user_data.get("id")
            if user_id is None:
                user_id = 0  # Default fallback for missing IDs
            members.append(User(
                id=user_id,
                first_name=user_data.get("first_name", "") or "",
                last_name=user_data.get("last_name", "") or "",
                email=user_data.get("email"),
                picture=user_data.get("picture", {}).get("medium") if user_data.get("picture") else None
            ))
        
        # Parse updated_at
        updated_at_str = group_data.get("updated_at", "")
        if updated_at_str:
            updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
        else:
            updated_at = datetime.now()
        
        # Ensure group ID is valid
        group_id = group_data.get("id")
        if group_id is None:
            raise ValueError("Group missing required 'id' field")
        
        # Ensure group_type is valid
        group_type = group_data.get("group_type") or "other"
        if not isinstance(group_type, str):
            group_type = "other"
        
        return Group(
            id=group_id,
            name=group_data.get("name", ""),
            group_type=group_type,
            updated_at=updated_at,
            simplify_by_default=group_data.get("simplify_by_default", False),
            members=members
        )
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """
        Fetch all data from Splitwise API.
        
        Returns:
            Dictionary with 'expenses', 'groups', 'current_user', 'friends'
        """
        current_user = self.get_current_user()
        groups = self.get_groups()
        expenses = self.get_expenses()
        friends = self.get_friends()
        
        return {
            "current_user": current_user,
            "groups": groups,
            "expenses": expenses,
            "friends": friends
        }

