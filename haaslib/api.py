from __future__ import annotations

import copy
import dataclasses
import random
from abc import ABC, abstractmethod, abstractproperty
from typing import (
    Any,
    Collection,
    Generic,
    Iterable,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    cast,
)

import requests
from pydantic import BaseModel, TypeAdapter

from haaslib.domain import HaaslibExcpetion
from haaslib.model import (
    ApiResponse,
    AuthenticatedSessionResponse,
    CloudMarket,
    CreateLabRequest,
    GetBacktestResultRequest,
    HaasScriptItemWithDependencies,
    PaginatedResponse,
    StartLabExecutionRequest,
    UserAccount,
    UserLabBacktestResult,
    UserLabDetails,
)

ApiResponseData = TypeVar("ApiResponseData", bound=BaseModel | Collection[BaseModel])
HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User"]


class HaasApiError(HaaslibExcpetion):
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


class SyncExecutor(Protocol, Generic[State]):
    def execute(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponseData:
        """
        Executes any request to Haas API and serialized it's reponse

        :param endpoint: Actual Haas API endpoint
        :param response_type: Pydantic class for response deserialization
        :param query_params: Endpoint parameters
        :raises HaasApiError: If API returned any error
        :return: API response deserialized into `response_type`
        """
        ...


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class RequestsExecutor(Generic[State]):
    host: str
    port: int
    state: State
    protocol: Literal["http", "https"] = dataclasses.field(default="http")

    def authenticate(
        self: RequestsExecutor[Guest], email: str, password: str
    ) -> RequestsExecutor[Authenticated]:
        """
        Creates authenticated session in Haas API

        :param email: Email used to login into Web UI
        :param password: Password used to login into Web UI
        :raises HaasApiError: If credentials are incorrect
        """
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
        if not resp.success:
            raise HaasApiError(resp.error or "Failed to login with credentials")

        resp = self._execute_inner(
            "User",
            response_type=AuthenticatedSessionResponse,
            query_params={
                "channel": "LOGIN_WITH_ONE_TIME_CODE",
                "email": email,
                "pincode": random.randint(100_000, 200_000),
                "interfaceKey": interface_key,
            },
        )
        if not resp.success:
            raise HaasApiError(resp.error or "Failed to login")

        assert resp.data is not None

        state = Authenticated(
            interface_key=interface_key, user_id=resp.data.data.user_id
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
        """
        Executes any request to Haas API and serialized it's reponse

        :param endpoint: Actual Haas API endpoint
        :param response_type: Pydantic class for response deserialization
        :param query_params: Endpoint parameters
        :raises HaasApiError: If API returned any error
        :return: API response deserialized into `response_type`
        """
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

        if not resp.success:
            raise HaasApiError(resp.error or "Request failed with empty error message")

        assert resp.data is not None

        return resp.data

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
        print(f"Requesting {url=}")
        resp = requests.get(url, params=query_params)

        ta = TypeAdapter(ApiResponse[response_type])
        return ta.validate_python(resp.json())


def get_all_markets(executor: SyncExecutor[Any]) -> list[CloudMarket]:
    return executor.execute(
        endpoint="Price",
        response_type=list[CloudMarket],
        query_params={"channel": "MARKETLIST"},
    )


def get_all_markets_by_pricesource(
    executor: SyncExecutor[Any], price_source: str
) -> list[CloudMarket]:
    return executor.execute(
        endpoint="Price",
        response_type=list[CloudMarket],
        query_params={"channel": "MARKETLIST", "pricesource": price_source},
    )


def get_all_script_items(
    executor: SyncExecutor[Authenticated],
) -> list[HaasScriptItemWithDependencies]:
    return executor.execute(
        endpoint="HaasScript",
        response_type=list[HaasScriptItemWithDependencies],
        query_params={"channel": "GET_ALL_SCRIPT_ITEMS"},
    )


def get_accounts(executor: SyncExecutor[Authenticated]) -> list[UserAccount]:
    return executor.execute(
        endpoint="Account",
        response_type=list[UserAccount],
        query_params={"channel": "GET_ACCOUNTS"},
    )


def create_lab(
    executor: SyncExecutor[Authenticated], req: CreateLabRequest
) -> UserLabDetails:
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "CREATE_LAB",
            "scriptId": req.script_id,
            "name": req.name,
            "accountId": req.account_id,
            "market": req.market,
            "interval": req.interval,
            "style": req.style,
        },
    )


def start_lab_execution(
    executor: SyncExecutor[Authenticated], req: StartLabExecutionRequest
) -> UserLabDetails:
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "START_LAB_EXECUTION",
            "labid": req.lab_id,
            "startunix": req.start_unix,
            "endunix": req.end_unix,
            "sendemail": req.send_email,
        },
    )


def get_lab_details(
    executor: SyncExecutor[Authenticated], lab_id: str
) -> UserLabDetails:
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={"channel": "GET_LAB_DETAILS", "labid": lab_id},
    )


def update_lab_details(
    executor: SyncExecutor[Authenticated], details: UserLabDetails
) -> UserLabDetails:
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "UPDATE_LAB_DETAILS",
            "labid": details.lab_id,
            "name": details.name,
            "type": details.algorithm,
            "config": details.user_lab_config,
            "settings": details.haas_script_settings,
            "parameters": details.parameters,
        },
    )


def update_multiple_lab_details(
    executor: SyncExecutor[Authenticated], details: Iterable[UserLabDetails]
) -> list[UserLabDetails]:
    return [update_lab_details(executor, detail) for detail in details]


def get_backtest_result(
    executor: SyncExecutor[Authenticated], req: GetBacktestResultRequest
) -> PaginatedResponse[UserLabBacktestResult]:
    return executor.execute(
        endpoint="Labs",
        response_type=PaginatedResponse[UserLabBacktestResult],
        query_params={
            "channel": "GET_BACKTEST_RESULT_PAGE",
            "labid": req.lab_id,
            "nextpageid": req.next_page_id,
            "pagelength": req.page_lenght,
        },
    )
