"""
Parser for CSV and JSON exports from Splitwise.
"""
import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from decimal import Decimal

from models.schemas import Expense, User, Group, ExpenseRepayment


class FileParser:
    """Parser for Splitwise export files"""
    
    @staticmethod
    def parse_csv(file_path: str) -> Dict[str, Any]:
        """
        Parse CSV export from Splitwise.
        
        Expected CSV format (Splitwise export):
        - Expense ID, Description, Date, Cost, Currency, Category, Group, etc.
        """
        expenses = []
        groups = {}
        users = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Parse expense
                expense_id = int(row.get('Expense ID', 0))
                if expense_id == 0:
                    continue
                
                # Parse date
                date_str = row.get('Date', '')
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    date = datetime.now()
                
                # Parse cost
                cost_str = row.get('Cost', '0').replace(',', '')
                cost = Decimal(cost_str)
                
                # Parse currency
                currency = row.get('Currency', 'USD')
                
                # Parse group
                group_name = row.get('Group', '')
                group_id = None
                if group_name:
                    # Create or get group
                    if group_name not in groups:
                        groups[group_name] = {
                            'id': len(groups) + 1,
                            'name': group_name,
                            'group_type': 'other',
                            'updated_at': date,
                            'members': []
                        }
                    group_id = groups[group_name]['id']
                
                # Parse users (who paid, who owes)
                # This is simplified - actual CSV may have different format
                paid_by = row.get('Paid by', '')
                owed_by = row.get('Owed by', '')
                
                # Create user entries if needed
                if paid_by and paid_by not in users:
                    users[paid_by] = {
                        'id': len(users) + 1,
                        'first_name': paid_by.split()[0] if paid_by else 'Unknown',
                        'last_name': ' '.join(paid_by.split()[1:]) if len(paid_by.split()) > 1 else '',
                    }
                
                # Build users list for expense
                users_list = []
                if paid_by:
                    user_id = users[paid_by]['id']
                    users_list.append({
                        'user': {'id': user_id, 'first_name': paid_by},
                        'paid_share': str(cost),
                        'owed_share': '0'
                    })
                
                # Get user ID with fallback
                creator_id = 1  # Default
                if paid_by and paid_by in users:
                    creator_id = users[paid_by].get('id', 1)
                
                expense = Expense(
                    id=expense_id,
                    group_id=group_id,
                    description=row.get('Description', ''),
                    payment=row.get('Payment', '').lower() == 'true',
                    cost=cost,
                    currency_code=currency,
                    date=date,
                    created_by=User(
                        id=creator_id,
                        first_name=paid_by.split()[0] if paid_by else 'Unknown',
                        last_name=''
                    ),
                    users=users_list,
                    repayments=[],
                    category=row.get('Category', ''),
                    receipt=None,
                    deleted_at=None
                )
                expenses.append(expense)
        
        # Convert groups dict to list
        groups_list = []
        for group_data in groups.values():
            groups_list.append(Group(
                id=group_data['id'],
                name=group_data['name'],
                group_type=group_data['group_type'],
                updated_at=group_data['updated_at'],
                simplify_by_default=False,
                members=[]
            ))
        
        return {
            'expenses': expenses,
            'groups': groups_list,
            'current_user': {'id': 1, 'first_name': 'User', 'last_name': ''},
            'friends': []
        }
    
    @staticmethod
    def parse_json(file_path: str) -> Dict[str, Any]:
        """
        Parse JSON export from Splitwise.
        
        Expected JSON format matches Splitwise API response structure.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # If it's a direct API response format
        if 'expenses' in data or 'groups' in data:
            return data
        
        # If it's a custom export format, adapt as needed
        expenses = data.get('expenses', [])
        groups = data.get('groups', [])
        current_user = data.get('current_user', {'id': 1, 'first_name': 'User', 'last_name': ''})
        friends = data.get('friends', [])
        
        return {
            'expenses': expenses,
            'groups': groups,
            'current_user': current_user,
            'friends': friends
        }
    
    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """
        Auto-detect file type and parse.
        
        Args:
            file_path: Path to CSV or JSON file
        
        Returns:
            Dictionary with parsed data
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() == '.csv':
            return FileParser.parse_csv(file_path)
        elif path.suffix.lower() == '.json':
            return FileParser.parse_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}. Use .csv or .json")

