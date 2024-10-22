from __future__ import annotations

import copy
import dataclasses
import json
import random
from typing import (
    Any,
    Generic,
    Iterable,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    cast,
    List,
    Dict,
    Union,
)

import requests
from pydantic import BaseModel, TypeAdapter, ValidationError, create_model, ConfigDict
from pydantic.json import pydantic_encoder

from haaslib.logger import log
from haaslib.model import (
    AddBotFromLabRequest,
    CloudMarket,
    CreateBotRequest,
    CreateLabRequest,
    GetBacktestResultRequest,
    HaasBot,
    HaasScriptItemWithDependencies,
    PaginatedResponse,
    StartLabExecutionRequest,
    UserAccount,
    UserLabBacktestResult,
    UserLabDetails,
    UserLabRecord,
)

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

State = TypeVar("State", bound=Guest | Authenticated)

class ApiResponse(BaseModel, Generic[ApiResponseData]):
    Success: bool
    Error: Optional[str] = None
    Data: Optional[ApiResponseData] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class SyncExecutor(Protocol, Generic[State]):
    def execute(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponseData:
        ...

@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class RequestsExecutor(Generic[State]):
    host: str
    port: int
    state: State
    protocol: Literal["http"] = dataclasses.field(default="http")

    def authenticate(
        self: RequestsExecutor[Guest], email: str, password: str
    ) -> RequestsExecutor[Authenticated]:
        interface_key = "".join(f"{random.randint(0, 100)}" for _ in range(10))
        resp = self._execute_inner(
            "User",
            response_type=dict,
            query_params={
                "channel": "LOGIN_WITH_CREDENTIALS",
                "email": email,
                "password": password,
                "interfaceKey": interface_key,
            },
        )
        if not resp.Success:
            raise HaasApiError(resp.Error or "Failed to login with credentials")

        resp = self._execute_inner(
            "User",
            response_type=dict,
            query_params={
                "channel": "LOGIN_WITH_ONE_TIME_CODE",
                "email": email,
                "pincode": random.randint(100_000, 200_000),
                "interfaceKey": interface_key,
            },
        )
        if not resp.Success:
            raise HaasApiError(resp.Error or "Failed to login")

        assert resp.Data is not None

        state = Authenticated(
            interface_key=interface_key, user_id=resp.Data.get("UserId")
        )

        return RequestsExecutor(
            host=self.host, port=self.port, state=state, protocol=self.protocol
        )

    def execute(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponseData:
        match self.state:
            case Authenticated():
                resp = cast(
                    RequestsExecutor[Authenticated], self
                )._execute_authenticated(endpoint, response_type, query_params)
            case Guest():
                resp = cast(RequestsExecutor[Guest], self)._execute_guest(
                    endpoint, response_type, query_params
                )
            case _:
                raise ValueError(f"Unknown auth state: {self.state}")

        if not resp.Success:
            raise HaasApiError(resp.Error or "Unknown error occurred")

        assert resp.Data is not None
        return resp.Data

    def _execute_authenticated(
        self: RequestsExecutor[Authenticated],
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        if query_params is None:
            query_params = {}
        else:
            query_params = copy.deepcopy(query_params)

        query_params["userid"] = self.state.user_id
        query_params["interfacekey"] = self.state.interface_key

        return self._execute_inner(endpoint, response_type, query_params)

    def _execute_guest(
        self: RequestsExecutor[Guest],
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        return self._execute_inner(endpoint, response_type, query_params)

    def _execute_inner(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        url = f"{self.protocol}://{self.host}:{self.port}/{endpoint}API.php"
        log.debug(
            f"[{self.state.__class__.__name__}]: Requesting {url=} with {query_params=}"
        )
        if query_params:
            query_params = query_params.copy()
            for key in query_params.keys():
                value = query_params[key]
                if isinstance(value, (str, int, float, bool, type(None))):
                    continue

                if isinstance(value, list):
                    log.debug(f"Converting to JSON string list `{key}` field")
                    query_params[key] = json.dumps(
                        value, default=self._custom_encoder(by_alias=True)
                    )

                if isinstance(value, BaseModel):
                    log.debug(f"Converting to JSON string pydantic `{key}` field")
                    query_params[key] = value.model_dump_json(by_alias=True)

        resp = requests.get(url, params=query_params)
        resp.raise_for_status()

        response_model = create_model(
            f"DynamicApiResponse",
            __base__=ApiResponse,
            Data=(Optional[response_type], None)
        )
        ta = TypeAdapter(response_model)

        try:
            return ta.validate_python(resp.json())
        except ValidationError:
            log.error(f"Failed to request: {resp.content}")
            raise

    @staticmethod
    def _custom_encoder(**kwargs):
        def base_encoder(obj):
            if isinstance(obj, BaseModel):
                return obj.model_dump(**kwargs)
            else:
                return pydantic_encoder(obj)

        return base_encoder

def get_all_markets_by_pricesource(executor: RequestsExecutor[Authenticated], price_source: str) -> List[CloudMarket]:
    return executor.execute(
        endpoint="Price",
        response_type=List[CloudMarket],
        query_params={"channel": "MARKETLIST", "pricesource": price_source},
    )

__all__ = ['RequestsExecutor', 'get_all_markets_by_pricesource', 'HaasApiError', 'Guest', 'Authenticated']
