from __future__ import annotations

import dataclasses
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

State = TypeVar("State")
ApiResponseData = TypeVar("ApiResponseData", bound=BaseModel | Collection[BaseModel])


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


class SyncExecutor(Protocol, Generic[State]):
    def execute(
        self,
        uri: str,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponseData: ...


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class RequestsExecutor(Generic[State]):
    host: str
    port: int
    state: State
    protocol: Literal["http", "https"] = dataclasses.field(default="http")

    def authenticate(
        self: RequestsExecutor[Guest],
    ) -> RequestsExecutor[Authenticated]: ...

    def execute(
        self,
        uri: str,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponseData:
        match self.state:
            case Authenticated():
                resp = cast(
                    RequestsExecutor[Authenticated], self
                )._execute_authenticated(uri, response_type, query_params)
            case Guest():
                resp = cast(RequestsExecutor[Guest], self)._execute_guest(
                    uri, response_type, query_params
                )
            case _:
                raise ValueError(f"Unknown auth state: {self.state}")

        if resp.success:
            return resp.data

        raise HaasApiError(resp.error)

    def _execute_authenticated(
        self: RequestsExecutor[Authenticated],
        uri: str,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        return self._execute_inner(uri, response_type, query_params)

    def _execute_guest(
        self: RequestsExecutor[Guest],
        uri: str,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        return self._execute_inner(uri, response_type, query_params)

    def _execute_inner(
        self,
        uri: str,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        url = f"{self.protocol}://{self.host}:{self.port}/{uri}"
        print(f"{url=}")
        resp = requests.get(url, params=query_params)
        ta = TypeAdapter(ApiResponse[response_type])
        return ta.validate_python(resp.json())

    def _wrap_with_credentials(self: RequestsExecutor[Authenticated], uri: str) -> str:
        return ""


def get_all_markets(executor: SyncExecutor[Any]) -> list[CloudMarket]:
    return executor.execute(
        uri="PriceAPI.php",
        response_type=list[CloudMarket],
        query_params={"channel": "MARKETLIST"},
    )


def get_all_markets_by_pricesource(
    executor: SyncExecutor[Any], price_source: str
) -> list[CloudMarket]:
    return executor.execute(
        uri=f"PriceAPI.php",
        response_type=list[CloudMarket],
        query_params={"channel": "MARKETLIST", "pricesource": price_source},
    )


def get_all_script_items(
    executor: SyncExecutor[Authenticated],
) -> list[HaasScriptItemWithDependencies]:
    return executor.execute(
        uri="HaasScriptAPI.php",
        response_type=list[HaasScriptItemWithDependencies],
        query_params={"channel": "GET_ALL_SCRIPT_ITEMS"},
    )


def get_accounts(executor: SyncExecutor[Authenticated]) -> list[UserAccount]:
    return executor.execute(
        uri="AccountAPI.php",
        response_type=list[UserAccount],
        query_params={"channel": "GET_ACCOUNTS"},
    )


def create_lab(
    executor: SyncExecutor[Authenticated], req: CreateLabRequest
) -> UserLabDetails:
    return executor.execute(
        uri=f"LabsAPI.php",
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
        uri="LabsAPI.php?",
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
        uri="LabsAPI.php",
        response_type=UserLabDetails,
        query_params={"channel": "GET_LAB_DETAILS", "labid": lab_id},
    )


def update_lab_details(
    executor: SyncExecutor[Authenticated], details: UserLabDetails
) -> UserLabDetails:
    return executor.execute(
        uri="LabsAPI.php",
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
        uri="LabsAPI.php",
        response_type=PaginatedResponse[UserLabBacktestResult],
        query_params={
            "channel": "GET_BACKTEST_RESULT_PAGE",
            "labid": req.lab_id,
            "nextpageid": req.next_page_id,
            "pagelength": req.page_lenght,
        },
    )
