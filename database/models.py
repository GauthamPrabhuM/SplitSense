"""
SQLAlchemy models for PostgreSQL database.
"""
from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class ExpenseModel(Base):
    """Expense model for PostgreSQL"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    description = Column(Text, nullable=False)
    payment = Column(Boolean, default=False)
    cost = Column(Numeric(10, 2), nullable=False)
    currency_code = Column(String(3), nullable=False, default="USD")
    date = Column(DateTime, nullable=False)
    category = Column(String(100), nullable=True)
    created_by_id = Column(Integer, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    group = relationship("GroupModel", back_populates="expenses")


class GroupModel(Base):
    """Group model for PostgreSQL"""
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    group_type = Column(String(50), nullable=True, default="other")
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    expenses = relationship("ExpenseModel", back_populates="group")


class UserSessionModel(Base):
    """User session model for OAuth tokens (optional - for multi-user support)"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    access_token = Column(Text, nullable=True)  # Encrypted in production
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

