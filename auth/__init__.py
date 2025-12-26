"""
Authentication module for Splitwise OAuth integration.
"""
from auth.oauth import SplitwiseOAuth, generate_oauth_state, validate_oauth_state, clear_oauth_state
from auth.sessions import (
    session_manager,
    SessionManager,
    UserSession,
    SESSION_COOKIE_NAME,
    get_cookie_settings,
)
from auth.middleware import (
    get_current_user,
    get_optional_user,
    set_session_cookie,
    clear_session_cookie,
    get_user_identifier,
    AuthenticationError,
    AuthorizationError,
)

__all__ = [
    # OAuth
    "SplitwiseOAuth",
    "generate_oauth_state",
    "validate_oauth_state",
    "clear_oauth_state",
    # Sessions
    "session_manager",
    "SessionManager",
    "UserSession",
    "SESSION_COOKIE_NAME",
    "get_cookie_settings",
    # Middleware/Dependencies
    "get_current_user",
    "get_optional_user",
    "set_session_cookie",
    "clear_session_cookie",
    "get_user_identifier",
    "AuthenticationError",
    "AuthorizationError",
]

