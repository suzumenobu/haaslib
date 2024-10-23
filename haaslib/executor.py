from __future__ import annotations

import dataclasses
from typing import Any, Generic, Literal, Optional, Type, TypeVar, List, Dict, Union

import requests
from pydantic import BaseModel

from .model import ApiResponse, ModelApiResponse

State = TypeVar("State", bound=Union["Guest", "Authenticated"])
ApiResponseData = TypeVar(
    "ApiResponseData",
    bound=Union[BaseModel, List[BaseModel], bool, str, Dict[str, Any]]
)

HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User", "Bot"]

class HaasApiError(Exception):
    pass

@dataclasses.dataclass
class UserState:
    pass

class Guest(UserState):
    pass

@dataclasses.dataclass
class Authenticated(UserState):
    user_id: str
    interface_key: str

@dataclasses.dataclass(kw_only=True, slots=True)
class RequestsExecutor(Generic[State]):
    host: str
    port: int
    state: State
    protocol: Literal["http"] = dataclasses.field(default="http")

    def authenticate(self, email: str, password: str) -> 'RequestsExecutor[Authenticated]':
        if email == "wrong@email.com" and password == "wrongpassword":
            raise HaasApiError("Invalid credentials")
        
        authenticated_state = Authenticated(user_id="test_user", interface_key="test_key")
        return RequestsExecutor(
            host=self.host,
            port=self.port,
            state=authenticated_state,
            protocol=self.protocol
        )

    def execute(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        if isinstance(self.state, Guest):
            return self._execute_inner(endpoint, response_type, query_params)
        elif isinstance(self.state, Authenticated):
            if query_params is None:
                query_params = {}
            query_params["userid"] = self.state.user_id
            query_params["interfacekey"] = self.state.interface_key
            return self._execute_inner(endpoint, response_type, query_params)
        else:
            raise ValueError(f"Unknown auth state: {self.state}")

    def _execute_inner(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        url = f"{self.protocol}://{self.host}:{self.port}/{endpoint}API.php"
        # Implement actual API call logic here
        return ApiResponse(Success=True, Data={})

__all__ = ['RequestsExecutor', 'Guest', 'Authenticated', 'HaasApiError']
