from typing import Optional

class HaaslibException(Exception):
    """Base exception for haaslib"""
    pass

class HaasApiError(HaaslibException):
    """Base exception for API errors"""
    def __init__(self, message: str, response: Optional[dict] = None, status_code: Optional[int] = None):
        super().__init__(message)
        self.response = response
        self.status_code = status_code
class RateLimitError(HaasApiError):
    """Raised when rate limit is exceeded"""
    def __init__(self, retry_after: float, response: Optional[dict] = None, status_code: Optional[int] = None):
        super().__init__("Rate limit exceeded", response, status_code)
        self.retry_after = retry_after
class AuthenticationError(HaasApiError):
    """Raised when authentication fails"""
    pass

class LabError(HaasApiError):
    """Raised when lab operations fail"""
    pass

class MarketError(HaasApiError):
    """Raised when market operations fail"""
    pass

class AccountError(HaasApiError):
    """Raised when account operations fail"""
    pass

class BotError(HaasApiError):
    """Raised when bot operations fail"""
    pass
