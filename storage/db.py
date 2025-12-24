"""
Optional storage layer using DuckDB.
"""
from typing import List, Optional
import duckdb
from pathlib import Path

from models.schemas import Expense, Group


class StorageManager:
    """Manage data storage using DuckDB"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize storage manager.
        
        Args:
            db_path: Path to DuckDB file (None for in-memory)
        """
        if db_path:
            self.conn = duckdb.connect(db_path)
        else:
            self.conn = duckdb.connect()
        
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables if they don't exist"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                group_id INTEGER,
                description TEXT,
                payment BOOLEAN,
                cost DECIMAL(10, 2),
                currency_code TEXT,
                date TIMESTAMP,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                name TEXT,
                group_type TEXT,
                updated_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def store_expenses(self, expenses: List[Expense]):
        """Store expenses in database"""
        # Clear existing data
        self.conn.execute("DELETE FROM expenses")
        
        # Insert expenses
        for expense in expenses:
            if expense.deleted_at:
                continue
            
            self.conn.execute("""
                INSERT INTO expenses 
                (id, group_id, description, payment, cost, currency_code, date, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                expense.id,
                expense.group_id,
                expense.description,
                expense.payment,
                float(expense.cost),
                expense.currency_code,
                expense.date,
                expense.category
            ))
    
    def store_groups(self, groups: List[Group]):
        """Store groups in database"""
        # Clear existing data
        self.conn.execute("DELETE FROM groups")
        
        # Insert groups
        for group in groups:
            self.conn.execute("""
                INSERT INTO groups (id, name, group_type, updated_at)
                VALUES (?, ?, ?, ?)
            """, (
                group.id,
                group.name,
                group.group_type,
                group.updated_at
            ))
    
    def query_expenses(self, query: str) -> List[dict]:
        """Execute custom query on expenses"""
        return self.conn.execute(query).fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()

