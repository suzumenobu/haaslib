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
from pydantic import BaseModel, ValidationError
import logging
import json
import os
import random

from .models.base import ApiResponse, ModelApiResponse
from .exceptions import HaasApiError, AuthenticationError
from . import logger
from .rate_limiter import RateLimiter  # Add this import
from .models.auth import AuthResponse  # Add this import
from .models.auth import AppLoginDetails  # Add this import
from .models.market import MarketListResponse

@dataclasses.dataclass
class Guest:
    """Represents an unauthenticated state"""
    pass

@dataclasses.dataclass
class Authenticated:
    """Represents an authenticated state"""
    user_id: str  # Added user_id
    interface_secret: str  # Changed from token to interface_secret

# Define TypeVar after the classes are defined
State = TypeVar("State", Guest, Authenticated)
HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User", "Bot"]

class RequestsExecutor(Generic[State]):
    """Executes API requests with retry logic and state management"""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        port: Optional[str] = None,
        state: Optional[State] = None  # Added state parameter
    ) -> None:
        """Initialize the executor with credentials"""
        self.base_url = base_url or os.getenv('HAAS_API_HOST')  # Changed from HAAS_API_URL
        self.email = email or os.getenv('HAAS_API_EMAIL')       # Changed from HAAS_TEST_EMAIL
        self.password = password or os.getenv('HAAS_API_PASSWORD')  # Changed from HAAS_TEST_PASSWORD
        self.port = port or os.getenv('HAAS_API_PORT', '8090')     # Changed default port
        self.state = state or Guest()  # Initialize state
        
        if not all([self.base_url, self.email, self.password]):
            raise ValueError("Missing required credentials")
            
        self.logger = logging.getLogger('haaslib')
        self.session = requests.Session()
        
        self.logger.debug(f"Initialized with base URL: {self.base_url}:{self.port}")
        
        self.max_retries = 3
        
        # Add rate limiter
        self.rate_limiter = RateLimiter()
        self.rate_limiter.requests_per_second = 0.5

    def set_debug(self, enabled: bool) -> None:
        """Enable or disable debug logging"""
        self.debug = enabled
        self.logger.debug(f"Debug mode {'enabled' if enabled else 'disabled'}")
    
    def execute(
        self,
        endpoint: str,
        response_type: Type[T],
        query_params: Optional[Dict] = None
    ) -> T:
        """Execute API request with retries"""
        max_attempts = 3
        attempt = 1
        
        while attempt <= max_attempts:
            try:
                response = self._make_request(endpoint, query_params)
                
                # Debug log the raw response
                self.logger.debug(f"Raw API Response: {response}...")  # First 1000 chars
                
                response_json = response
                
                # Debug log the parsed JSON
                self.logger.debug(f"Parsed JSON: {json.dumps(response_json, indent=2)[:1000]}...")
                
                if response_type == MarketListResponse:
                    # Ensure Data is a list
                    if 'Data' in response_json and not isinstance(response_json['Data'], list):
                        response_json['Data'] = [response_json['Data']]
                    
                    # Debug log the Data structure
                    if response_json.get('Data'):
                        self.logger.debug(f"First market in Data: {response_json['Data'][0]}")
                
                return response_type(**response_json)
                
            except ValidationError as e:
                self.logger.error(f"Attempt {attempt} failed: {str(e)}")
                if attempt == max_attempts:
                    raise
                attempt += 1
                time.sleep(1)  # Wait before retry

    def authenticate(
        self: RequestsExecutor[Guest]
    ) -> RequestsExecutor[Authenticated]:
        """Creates authenticated session in Haas API"""
        try:
            # 1. Generate interface key
            interface_secret = "".join(f"{random.randint(0, 100)}" for _ in range(10))
            self.logger.debug(f"Generated interface key: {interface_secret}")
            
            # 2. Initial login
            login_resp = self._make_request(
                endpoint="User",
                query_params={
                    "channel": "LOGIN_WITH_CREDENTIALS",
                    "email": self.email,
                    "password": self.password,
                    "interfaceKey": interface_secret,
                },
            )
            
            if not login_resp.get('Success'):
                raise AuthenticationError(f"Initial login failed: {login_resp.get('Error')}")

            # 3. One-time code authentication
            auth_resp = self._make_request(
                endpoint="User",
                query_params={
                    "channel": "LOGIN_WITH_ONE_TIME_CODE",
                    "email": self.email,
                    "pincode": random.randint(100_000, 200_000),
                    "interfaceKey": interface_secret,
                },
            )
            
            if not auth_resp.get('Success'):
                raise AuthenticationError(f"One-time code auth failed: {auth_resp.get('Error')}")

            # 4. Extract user data from nested structure
            data = auth_resp.get('Data', {})
            d_data = data.get('D', {})
            
            user_id = d_data.get('UserId')
            interface_secret = d_data.get('InterfaceSecret')  # Changed from InterfaceKey to InterfaceSecret

            if not user_id or not interface_secret:
                self.logger.error(f"Missing required fields. Full response: {auth_resp}")
                raise AuthenticationError("Missing required fields in response")

            self.logger.info(f"Successfully authenticated user: {user_id}")
            
            # 5. Create new authenticated executor
            return RequestsExecutor(
                base_url=self.base_url,
                port=self.port,
                email=self.email,
                password=self.password,
                state=Authenticated(
                    user_id=user_id,
                    interface_secret=interface_secret
                )
            )
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationError(f"Authentication failed: {str(e)}")

    def _make_request(self, endpoint: str, query_params: Optional[dict] = None) -> dict:
        """Make HTTP request to API endpoint"""
        url = f"http://{self.base_url}:{self.port}/{endpoint}API.php"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if isinstance(self.state, Authenticated):
            headers["Authorization"] = f"Bearer {self.state.interface_secret}"
            
        self.logger.debug(f"Making request to: {url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Query params: {query_params}")
        
        try:
            response = requests.get(url, params=query_params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise

__all__ = ['RequestsExecutor', 'Guest', 'Authenticated', 'HaasApiError']
