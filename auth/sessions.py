"""
Secure session management for user authentication.
Uses signed cookies with user-scoped data storage.
"""
import os
import secrets
import hashlib
import hmac
import json
import time
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from threading import Lock

from models.schemas import Expense, Group, AllInsights


# Session configuration
SESSION_COOKIE_NAME = "splitsense_session"
SESSION_EXPIRY_HOURS = 24  # Sessions expire after 24 hours
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", secrets.token_hex(32))


@dataclass
class UserSession:
    """Represents a user's session with their data"""
    session_id: str
    user_id: int
    splitwise_user_id: int
    first_name: str
    last_name: str
    email: Optional[str]
    access_token: str  # Splitwise OAuth token
    created_at: datetime
    last_accessed: datetime
    expires_at: datetime
    
    # User's data (isolated per user)
    expenses: List[Expense] = field(default_factory=list)
    groups: List[Group] = field(default_factory=list)
    insights: Optional[AllInsights] = None
    friend_balances: List[dict] = field(default_factory=list)
    
    def is_expired(self) -> bool:
        """Check if session has expired"""
        return datetime.utcnow() > self.expires_at
    
    def refresh(self):
        """Refresh session expiry time"""
        self.last_accessed = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(hours=SESSION_EXPIRY_HOURS)


class SessionManager:
    """
    Thread-safe session manager with user-scoped data storage.
    In production, replace with Redis or database-backed storage.
    """
    
    def __init__(self):
        self._sessions: Dict[str, UserSession] = {}
        self._user_sessions: Dict[int, str] = {}  # user_id -> session_id mapping
        self._lock = Lock()
    
    def _generate_session_id(self) -> str:
        """Generate a cryptographically secure session ID"""
        return secrets.token_urlsafe(32)
    
    def _sign_session_id(self, session_id: str) -> str:
        """Sign session ID with HMAC for integrity verification"""
        signature = hmac.new(
            SESSION_SECRET_KEY.encode(),
            session_id.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{session_id}.{signature}"
    
    def _verify_session_id(self, signed_session: str) -> Optional[str]:
        """Verify signed session ID and return original if valid"""
        try:
            parts = signed_session.rsplit('.', 1)
            if len(parts) != 2:
                return None
            
            session_id, signature = parts
            expected_signature = hmac.new(
                SESSION_SECRET_KEY.encode(),
                session_id.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if hmac.compare_digest(signature, expected_signature):
                return session_id
            return None
        except Exception:
            return None
    
    def create_session(
        self,
        splitwise_user_id: int,
        first_name: str,
        last_name: str,
        email: Optional[str],
        access_token: str,
    ) -> str:
        """
        Create a new session for a user.
        Returns signed session ID to be stored in cookie.
        """
        with self._lock:
            # Remove any existing session for this user
            if splitwise_user_id in self._user_sessions:
                old_session_id = self._user_sessions[splitwise_user_id]
                self._sessions.pop(old_session_id, None)
            
            session_id = self._generate_session_id()
            now = datetime.utcnow()
            
            session = UserSession(
                session_id=session_id,
                user_id=splitwise_user_id,  # Use Splitwise user ID
                splitwise_user_id=splitwise_user_id,
                first_name=first_name,
                last_name=last_name or "",
                email=email,
                access_token=access_token,
                created_at=now,
                last_accessed=now,
                expires_at=now + timedelta(hours=SESSION_EXPIRY_HOURS),
            )
            
            self._sessions[session_id] = session
            self._user_sessions[splitwise_user_id] = session_id
            
            return self._sign_session_id(session_id)
    
    def get_session(self, signed_session: str) -> Optional[UserSession]:
        """Get session by signed session ID"""
        session_id = self._verify_session_id(signed_session)
        if not session_id:
            return None
        
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None
            
            if session.is_expired():
                self.destroy_session(signed_session)
                return None
            
            # Refresh session on access
            session.refresh()
            return session
    
    def destroy_session(self, signed_session: str) -> bool:
        """Destroy a session"""
        session_id = self._verify_session_id(signed_session)
        if not session_id:
            return False
        
        with self._lock:
            session = self._sessions.pop(session_id, None)
            if session:
                self._user_sessions.pop(session.splitwise_user_id, None)
                return True
            return False
    
    def update_session_data(
        self,
        signed_session: str,
        expenses: Optional[List[Expense]] = None,
        groups: Optional[List[Group]] = None,
        insights: Optional[AllInsights] = None,
        friend_balances: Optional[List[dict]] = None,
    ) -> bool:
        """Update user data in session"""
        session = self.get_session(signed_session)
        if not session:
            return False
        
        with self._lock:
            if expenses is not None:
                session.expenses = expenses
            if groups is not None:
                session.groups = groups
            if insights is not None:
                session.insights = insights
            if friend_balances is not None:
                session.friend_balances = friend_balances
            return True
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions (call periodically)"""
        with self._lock:
            expired = [
                sid for sid, session in self._sessions.items()
                if session.is_expired()
            ]
            for sid in expired:
                session = self._sessions.pop(sid, None)
                if session:
                    self._user_sessions.pop(session.splitwise_user_id, None)
    
    def get_session_count(self) -> int:
        """Get number of active sessions"""
        with self._lock:
            return len(self._sessions)


# Global session manager instance
session_manager = SessionManager()


def get_cookie_settings() -> dict:
    """Get secure cookie settings based on environment"""
    is_production = os.getenv("ENVIRONMENT") == "production"
    
    return {
        "key": SESSION_COOKIE_NAME,
        "httponly": True,  # Prevent JavaScript access
        "secure": is_production,  # HTTPS only in production
        "samesite": "lax",  # CSRF protection
        "max_age": SESSION_EXPIRY_HOURS * 3600,  # Cookie expiry in seconds
        "path": "/",
    }
