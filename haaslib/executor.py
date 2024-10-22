import logging
from typing import Generic, Type, Optional, TypeVar, Any, Dict, List
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from .api import SyncExecutor, State, Guest, Authenticated, HaasApiError, BaseModel, HaasApiEndpoint, ApiResponseData
from .logging_config import logger
from .config import config

T = TypeVar('T')

class RequestsExecutor(SyncExecutor[Guest]):
    def __init__(self, host: str = config.API_HOST, port: int = config.API_PORT, state: Guest = Guest()):
        self.base_url = f"http://{host}:{port}"  # Changed to HTTP
        self.state = state
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retry))  # Changed to HTTP

    def authenticate(self, email: str, password: str) -> 'RequestsExecutor[Authenticated]':
        try:
            response = self.execute(
                endpoint="User",
                response_type=Dict[str, Any],
                query_params={
                    "channel": "LOGIN",
                    "email": email,
                    "password": password
                }
            )
            if not response.get('Success'):
                raise HaasApiError(f"Authentication failed: {response.get('Error')}")
            
            user_id = response['Data']['UserId']
            interface_key = response['Data']['InterfaceSecret']
            authenticated_state = Authenticated(user_id=user_id, interface_key=interface_key)
            return RequestsExecutor(state=authenticated_state)
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise HaasApiError(f"Authentication failed: {str(e)}")

    def execute(self, endpoint: HaasApiEndpoint, response_type: Type[T], query_params: Optional[Dict[str, Any]] = None) -> T:
        url = f"{self.base_url}/{endpoint}API.php"
        headers: Dict[str, str] = {}
        if isinstance(self.state, Authenticated):
            query_params = query_params or {}
            query_params.update({
                "userid": self.state.user_id,
                "interfacekey": self.state.interface_key
            })
        
        logger.debug(f"Executing request: URL={url}, Params={query_params}")
        try:
            response = self.session.get(url, params=query_params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            logger.debug(f"Raw API response: {data}")
            
            if not data.get('Success'):
                raise HaasApiError(f"API request failed: {data.get('Error')}")
            
            if isinstance(response_type, type) and issubclass(response_type, list):
                return response_type(data.get('Data', []))
            elif response_type == Dict[str, Any]:
                return data
            elif issubclass(response_type, ApiResponseData):
                return response_type.parse_obj(data.get('Data', {}))
            else:
                return data.get('Data')
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise HaasApiError(f"Request failed: {str(e)}")
        except ValueError as e:
            logger.error(f"Failed to parse response: {str(e)}")
            raise HaasApiError(f"Failed to parse response: {str(e)}")

__all__ = ['RequestsExecutor']
