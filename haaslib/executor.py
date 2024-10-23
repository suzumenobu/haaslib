from __future__ import annotations

import dataclasses
import time
from typing import (
    Any, 
    Generic, 
    Literal, 
    Optional, 
    Type, 
    TypeVar, 
    Dict, 
    Union,
    List,
)
from functools import wraps

import requests
from pydantic import BaseModel

from .models import ApiResponse, ModelApiResponse
from . import logger

State = TypeVar("State", bound=Union["Guest", "Authenticated"])
ApiResponseData = TypeVar(
    "ApiResponseData",
    bound=Union[BaseModel, List[BaseModel], bool, str, Dict[str, Any]]
)

HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User", "Bot"]

class HaasApiError(Exception):
    """Base exception for API errors"""
    pass

@dataclasses.dataclass
class UserState:
    """Base class for user states"""
    pass

class Guest(UserState):
    """Guest user state"""
    pass

@dataclasses.dataclass
class Authenticated(UserState):
    """Authenticated user state"""
    user_id: str
    interface_key: str

def rate_limit(calls: int, period: float):
    """Rate limiting decorator"""
    def decorator(func):
        last_reset = time.time()
        calls_made = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_reset, calls_made
            
            current_time = time.time()
            if current_time - last_reset > period:
                calls_made = 0
                last_reset = current_time
                
            if calls_made >= calls:
                sleep_time = period - (current_time - last_reset)
                if sleep_time > 0:
                    logger.debug(f"Rate limit reached. Sleeping for {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                calls_made = 0
                last_reset = time.time()
                
            calls_made += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

class RequestsExecutor(Generic[State]):
    """API executor with rate limiting and retries"""
    
    def __init__(
        self,
        host: str,
        port: int,
        state: State,
        protocol: str = "http",  # Default to http
        max_retries: int = 3,
        retry_delay: float = 1.0,
        rate_limit_calls: int = 60,
        rate_limit_period: float = 60.0,
    ):
        """Initialize the executor"""
        self.host = host
        self.port = port
        self.state = state
        self.protocol = "http"  # Force HTTP
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        
        # Initialize session
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self._session.mount('http://', adapter)

    @property
    def session(self) -> requests.Session:
        """Get the requests session"""
        if not hasattr(self, '_session') or self._session is None:
            self._session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
            self._session.mount('http://', adapter)
        return self._session

    @rate_limit(calls=60, period=60.0)
    def execute(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        """Execute API request with retries and rate limiting"""
        retries = 0
        last_error = None
        
        while retries < self.max_retries:
            try:
                return self._execute_inner(endpoint, response_type, query_params)
            except (requests.RequestException, HaasApiError) as e:
                last_error = e
                retries += 1
                if retries < self.max_retries:
                    sleep_time = self.retry_delay * (2 ** (retries - 1))
                    logger.warning(
                        f"Request failed: {e}. Retrying in {sleep_time:.2f}s "
                        f"(attempt {retries}/{self.max_retries})"
                    )
                    time.sleep(sleep_time)
                
        raise HaasApiError(f"Request failed after {self.max_retries} retries: {last_error}")

    def _execute_inner(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        """Execute a single API request"""
        url = f"{self.protocol}://{self.host}:{self.port}/{endpoint}API.php"
        
        try:
            response = self.session.get(url, params=query_params or {})
            response.raise_for_status()
            
            data = response.json()
            return ApiResponse(Success=True, Data=data.get('Data', {}))
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed: {e}")
            raise HaasApiError(f"Request failed: {e}") from e
        except Exception as e:
            logger.warning(f"Unexpected error: {e}")
            raise HaasApiError(f"Unexpected error: {e}") from e

    def authenticate(self, email: str, password: str) -> RequestsExecutor[Authenticated]:
        """Authenticate and return new executor with authenticated state"""
        response = self.execute(
            endpoint="User",
            response_type=dict,
            query_params={
                "channel": "AUTH",
                "email": email,
                "password": password
            }
        )
        
        if not response.Success:
            raise HaasApiError(f"Authentication failed: {response.Error}")
        
        # Handle empty response
        if not response.Data:
            raise HaasApiError("Authentication failed: No data returned")
        
        # Extract user ID and interface key
        user_id = response.Data.get('UserId')
        interface_key = response.Data.get('InterfaceKey')
        
        if not user_id or not interface_key:
            raise HaasApiError(
                f"Authentication failed: Missing required fields. Got: {response.Data}"
            )
        
        return RequestsExecutor[Authenticated](
            host=self.host,
            port=self.port,
            state=Authenticated(
                user_id=user_id,
                interface_key=interface_key
            ),
            protocol=self.protocol,
            max_retries=self.max_retries,
            retry_delay=self.retry_delay
        )

    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, '_session'):
            try:
                self._session.close()
            except Exception:
                pass

__all__ = ['RequestsExecutor', 'Guest', 'Authenticated', 'HaasApiError']
