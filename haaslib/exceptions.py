"""Custom exceptions for HaasLib"""
from typing import Optional, Any

class HaasLibError(Exception):
    """Base exception for all HaasLib errors"""
    pass

class HaasApiError(HaasLibError):
    """API-related errors"""
    def __init__(
        self,
        message: str,
        response: Optional[Any] = None,
        status_code: Optional[int] = None
    ):
        super().__init__(message)
        self.response = response
        self.status_code = status_code

class AuthenticationError(HaasApiError):
    """Authentication-related errors"""
    pass

class RateLimitError(HaasApiError):
    """Rate limit exceeded"""
    def __init__(self, retry_after: float):
        super().__init__("Rate limit exceeded")
        self.retry_after = retry_after

class ValidationError(HaasLibError):
    """Data validation errors"""
    pass

class ConfigurationError(HaasLibError):
    """Configuration-related errors"""
    pass
