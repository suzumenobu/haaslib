from __future__ import annotations

import dataclasses
from typing import Any, Generic, Iterable, Optional, Protocol, Type, TypeVar

import requests
from pydantic import BaseModel

from src.model import (
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
ApiResponse = TypeVar("ApiResponse")


class Executor(Protocol):
    def execute(self): ...


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
        response_type: Type[ApiResponse],
        query_params: Optional[dict] = None,
    ) -> ApiResponse: ...


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class RequestsExecutor(Generic[State]):
    address: str
    port: int
    protocol: str
    state: State

    def authenticate(
        self: RequestsExecutor[Guest],
    ) -> RequestsExecutor[Authenticated]: ...

    def execute(
        self,
        uri: str,
        response_type: Type[ApiResponse],
        query_params: Optional[dict] = None,
    ) -> ApiResponse: ...

    def _excute_authenticated(
        self: RequestsExecutor[Authenticated],
        uri: str,
        response_type: Type[ApiResponse],
    ) -> ApiResponse: ...

    def _excute_guest(
        self: RequestsExecutor[Guest], uri: str, response_type: Type[ApiResponse]
    ) -> ApiResponse: ...

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
