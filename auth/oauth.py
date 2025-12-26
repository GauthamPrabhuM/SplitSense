"""
OAuth 2.0 authentication for Splitwise integration.
Enables seamless login without manual API key entry.
"""
import os
import secrets
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs, urlparse
import httpx
from fastapi import HTTPException

from config import Config


class SplitwiseOAuth:
    """OAuth 2.0 client for Splitwise"""
    
    # Splitwise OAuth endpoints
    AUTHORIZATION_URL = "https://secure.splitwise.com/oauth/authorize"
    TOKEN_URL = "https://secure.splitwise.com/oauth/token"
    
    def __init__(self):
        """Initialize OAuth client with credentials from environment"""
        self.client_id = os.getenv("SPLITWISE_CLIENT_ID")
        self.client_secret = os.getenv("SPLITWISE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPLITWISE_REDIRECT_URI", "http://localhost:8000/auth/callback")
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "SPLITWISE_CLIENT_ID and SPLITWISE_CLIENT_SECRET must be set in environment variables. "
                "Get them from https://secure.splitwise.com/apps"
            )
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Generate authorization URL for OAuth flow.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Authorization URL to redirect user to
        """
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": state,
            # Note: Splitwise may not support scope parameter for OAuth 2.0
            # Removed scope to match standard OAuth 2.0 flow
        }
        
        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
        print(f"Generated OAuth URL with redirect_uri: {self.redirect_uri}")
        return auth_url
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from callback
            
        Returns:
            Dictionary with access_token, token_type, etc.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            
            if response.status_code != 200:
                error_detail = response.text
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to exchange code for token: {error_detail}"
                )
            
            return response.json()
    
    def get_access_token_from_env(self) -> Optional[str]:
        """
        Get access token from environment variable (for development/testing).
        
        Returns:
            Access token if available, None otherwise
        """
        return os.getenv("SPLITWISE_ACCESS_TOKEN")


# Session storage for OAuth state (in production, use Redis or database)
_oauth_states: Dict[str, str] = {}


def generate_oauth_state() -> str:
    """Generate and store OAuth state for CSRF protection"""
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = "pending"
    return state


def validate_oauth_state(state: str) -> bool:
    """Validate OAuth state parameter"""
    return state in _oauth_states


def clear_oauth_state(state: str):
    """Clear OAuth state after use"""
    _oauth_states.pop(state, None)

