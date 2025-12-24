"""
Configuration settings for the Splitwise Analysis Tool.
"""
import os
from typing import Optional


class Config:
    """Application configuration"""
    
    # API Settings
    SPLITWISE_API_BASE_URL = "https://secure.splitwise.com/api/v3.0"
    API_RATE_LIMIT_DELAY = 0.5  # seconds
    
    # Security Settings
    STORE_TOKENS = os.getenv("STORE_TOKENS", "false").lower() == "true"
    MASK_SENSITIVE_DATA = os.getenv("MASK_SENSITIVE_DATA", "true").lower() == "true"
    LOCAL_ONLY = os.getenv("LOCAL_ONLY", "true").lower() == "true"
    
    # Data Settings
    DEFAULT_BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USD")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    
    # Storage Settings
    USE_STORAGE = os.getenv("USE_STORAGE", "false").lower() == "true"
    STORAGE_PATH = os.getenv("STORAGE_PATH", "data/splitwise.db")
    
    @staticmethod
    def get_api_token() -> Optional[str]:
        """Get API token from environment variable"""
        token = os.getenv("SPLITWISE_API_TOKEN")
        if token and not Config.STORE_TOKENS:
            # Token should not be stored, only used temporarily
            return token
        return token
    
    @staticmethod
    def mask_sensitive_data(text: str, mask_char: str = "*") -> str:
        """Mask sensitive information if enabled"""
        if not Config.MASK_SENSITIVE_DATA:
            return text
        
        if len(text) > 4:
            return text[:2] + mask_char * (len(text) - 4) + text[-2:]
        return mask_char * len(text)

