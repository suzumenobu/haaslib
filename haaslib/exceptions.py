class HaaslibException(Exception):
    """Base exception for haaslib."""
    pass

class HaasApiError(HaaslibException):
    """Raised when there's an error in API calls."""
    pass

class HaasApiRateLimitError(HaasApiError):
    """Raised when the API rate limit is exceeded."""
    pass

class HaasApiAuthenticationError(HaasApiError):
    """Raised when there's an authentication error."""
    pass

class HaasConfigError(HaaslibException):
    """Raised when there's an error in configuration."""
    pass