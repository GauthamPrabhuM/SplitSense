"""
Authentication middleware and dependencies for FastAPI.
Enforces user authentication on protected endpoints.
"""
import os
from typing import Optional
from functools import wraps

from fastapi import Request, HTTPException, Depends, Response
from fastapi.responses import JSONResponse, RedirectResponse

from auth.sessions import (
    session_manager,
    UserSession,
    SESSION_COOKIE_NAME,
    get_cookie_settings,
)


class AuthenticationError(HTTPException):
    """Custom exception for authentication failures"""
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(status_code=401, detail=detail)


class AuthorizationError(HTTPException):
    """Custom exception for authorization failures"""
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status_code=403, detail=detail)


def get_session_from_request(request: Request) -> Optional[str]:
    """Extract session cookie from request"""
    return request.cookies.get(SESSION_COOKIE_NAME)


async def get_current_user(request: Request) -> UserSession:
    """
    FastAPI dependency to get the current authenticated user.
    Raises 401 if not authenticated.
    """
    signed_session = get_session_from_request(request)
    
    if not signed_session:
        raise AuthenticationError("No session cookie found. Please log in.")
    
    session = session_manager.get_session(signed_session)
    
    if not session:
        raise AuthenticationError("Session expired or invalid. Please log in again.")
    
    return session


async def get_optional_user(request: Request) -> Optional[UserSession]:
    """
    FastAPI dependency to optionally get the current user.
    Returns None if not authenticated (doesn't raise).
    """
    signed_session = get_session_from_request(request)
    
    if not signed_session:
        return None
    
    return session_manager.get_session(signed_session)


def set_session_cookie(response: Response, signed_session: str):
    """Set session cookie on response"""
    settings = get_cookie_settings()
    response.set_cookie(
        value=signed_session,
        **settings
    )


def clear_session_cookie(response: Response):
    """Clear session cookie from response"""
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/",
    )


class AuthMiddleware:
    """
    Middleware to add user info to request state.
    Does not enforce auth - that's done by dependencies.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Get request
            from starlette.requests import Request
            request = Request(scope, receive)
            
            # Try to get user from session
            signed_session = request.cookies.get(SESSION_COOKIE_NAME)
            if signed_session:
                session = session_manager.get_session(signed_session)
                if session:
                    scope["state"] = scope.get("state", {})
                    scope["state"]["user"] = session
        
        await self.app(scope, receive, send)


# Rate limiting per user (if slowapi is available)
def get_user_identifier(request: Request) -> str:
    """Get user identifier for rate limiting"""
    signed_session = get_session_from_request(request)
    if signed_session:
        session = session_manager.get_session(signed_session)
        if session:
            return f"user:{session.user_id}"
    
    # Fall back to IP address for unauthenticated requests
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return f"ip:{forwarded.split(',')[0].strip()}"
    
    client = request.client
    if client:
        return f"ip:{client.host}"
    
    return "ip:unknown"
