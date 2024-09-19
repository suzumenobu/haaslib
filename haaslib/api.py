from __future__ import annotations

import copy
import dataclasses
import json
import random
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
from pydantic import BaseModel, TypeAdapter, ValidationError
from pydantic.json import pydantic_encoder

from haaslib.exceptions import HaasApiError, HaasApiRateLimitError, HaasApiAuthenticationError
from haaslib.config import config
from haaslib.logger import log
from haaslib.model import (
    AddBotFromLabRequest,
    ApiResponse,
    AuthenticatedSessionResponse,
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
    UserLabDetails,
    UserLabRecord,
    BotOrder, BotPosition, BotRuntimeReport, BotResetConfig,
    BotOrderList, BotPositionList, BotClosedPositionList
)

ApiResponseData = TypeVar(
    "ApiResponseData", bound=BaseModel | Collection[BaseModel] | bool | str
)
"""Any response from Haas API should be `pydantic` model or collection of them."""

HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User", "Bot"]
"""Known Haas API endpoints"""


@dataclasses.dataclass
class UserState:
    """
    Base user API Session type.
    """

    pass


class Guest(UserState):
    """
    Default user session type.
    """

    pass


@dataclasses.dataclass
class Authenticated(UserState):
    """
    Authenticated user session required for the most of the endpoints.
    """

    user_id: str
    interface_key: str


State = TypeVar("State", bound=Guest | Authenticated)
"""Generic to mark user session typ"""


class SyncExecutor(Protocol, Generic[State]):
    """
    Main protocol for interaction with HaasAPI.
    """

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
    """First implementation of `SyncExecutor` based on `requests` library."""

    host: str
    """ Address of the Haas API."""

    port: int
    """ Port of the Haas API."""

    state: State
    """ User session state."""

    protocol: Literal["http"] = dataclasses.field(default="http")
    """Communication protocol (currently only http is valid)."""

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
            if query_params:
                req = {
                    k: v
                    for k, v in query_params.items()
                    if k not in ("userid", "interfacekey")
                }
            else:
                req = None

            msg = resp.error or "[No response]"

            raise HaasApiError(
                f"Failed to request {endpoint}API with {msg}. Input params: {req}"
            )

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

        ta = TypeAdapter(ApiResponse[response_type])

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


def get_all_markets(executor: SyncExecutor[Any]) -> list[CloudMarket]:
    """
    Retrieves information about all available markets.

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: List with all cloud markets
    """
    return executor.execute(
        endpoint="Price",
        response_type=list[CloudMarket],
        query_params={"channel": "MARKETLIST"},
    )


def get_all_markets_by_pricesource(
    executor: SyncExecutor[Any], price_source: str
) -> list[CloudMarket]:
    """
    Retrieves information about markets from a specific price source.

    :param executor: Executor for Haas API interaction
    :param price_source: The specific price source for which market information is requested
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: List with cloud markets with the given `price_source`
    """
    return executor.execute(
        endpoint="Price",
        response_type=list[CloudMarket],
        query_params={"channel": "MARKETLIST", "pricesource": price_source},
    )


def get_unique_pricesources(executor: SyncExecutor[Any]) -> set[str]:
    """
    Returns all unique price sources

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: Set of price sources
    """
    all_markets = get_all_markets(executor)
    return set(m.price_source for m in all_markets)


def get_all_scripts(
    executor: SyncExecutor[Authenticated],
) -> list[HaasScriptItemWithDependencies]:
    """
    Retrieves information about all script items for an authenticated user.

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: List with all available scripts
    """
    return executor.execute(
        endpoint="HaasScript",
        response_type=list[HaasScriptItemWithDependencies],
        query_params={"channel": "GET_ALL_SCRIPT_ITEMS"},
    )


def get_accounts(executor: SyncExecutor[Authenticated]) -> list[UserAccount]:
    """
    Retrieves information about user accounts for an authenticated user.

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: List with all available user accounts
    """
    return executor.execute(
        endpoint="Account",
        response_type=list[UserAccount],
        query_params={"channel": "GET_ACCOUNTS"},
    )


def create_lab(
    executor: SyncExecutor[Authenticated], req: CreateLabRequest
) -> UserLabDetails:
    """
    Creates a new lab for an authenticated user.

    Lab name could be duplicated
    Market Tag could be created from `CloudMarket`

    :param executor: Executor for Haas API interaction
    :param req: Details of the lab
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: Created lab details
    """
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "CREATE_LAB",
            "scriptId": req.script_id,
            "name": req.name,
            "accountId": req.account_id,
            "market": req.market.tag,
            "interval": req.interval,
            "style": req.default_price_data_style,
        },
    )


def start_lab_execution(
    executor: SyncExecutor[Authenticated], req: StartLabExecutionRequest
) -> UserLabDetails:
    """
    Starts the execution of a lab for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param req: Details for starting the lab execution
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: Started lab details
    """
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
    """
    Retrieves details about a specific lab for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param lab_id: The ID of the lab for which details are requested
    :raises HaasApiError: If lab not found
    :return: Lab details
    """
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={"channel": "GET_LAB_DETAILS", "labid": lab_id},
    )


def update_lab_details(
    executor: SyncExecutor[Authenticated], details: UserLabDetails
) -> UserLabDetails:
    """
    Updates details for a specific lab for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param details: The updated UserLabDetails for the lab.
    :raises HaasApiError: If requested lab not found
    :return: Updated lab details
    """
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
    """
    Updates details for multiple labs for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param details: Iterable with details to update
    :raises HaasApiError: If requested lab not found
    :return: Updated lab details
    """
    return [update_lab_details(executor, detail) for detail in details]


def get_backtest_result(
    executor: SyncExecutor[Authenticated], req: GetBacktestResultRequest
) -> PaginatedResponse[UserLabBacktestResult]:
    """
    Retrieves the backtest result for a specific lab for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param req: Required info for retrieving backtest result
    :raises HaasApiError: If requested lab not found
    :return: Backtes result
    """
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


def get_all_labs(executor: SyncExecutor[Authenticated]) -> list[UserLabDetails]:
    """
    Fetches all labs for the given session

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: Not found yet
    :return: List of the all labs details
    """
    return executor.execute(
        endpoint="Labs",
        response_type=list[UserLabRecord],  # type: ignore
        query_params={"channel": "GET_LABS"},
    )


def delete_lab(executor: SyncExecutor[Authenticated], lab_id: str):
    """
    Removes Lab with given id

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: Not found yet
    """
    return executor.execute(
        endpoint="Labs",
        response_type=bool,
        query_params={"channel": "DELETE_LAB", "labid": lab_id},
    )


def add_bot(executor: SyncExecutor[Authenticated], req: CreateBotRequest) -> HaasBot:
    """
    Creates new bot

    :param executor: Executor for Haas API interaction
    :param req: Details of bot creation
    :return: Created bot details
    """
    return executor.execute(
        endpoint="Bot",
        response_type=HaasBot,
        query_params={
            "channel": "ADD_BOT",
            "botname": req.bot_name,
            "scriptid": req.script.id,
            "scripttype": req.script.type,
            "accountid": req.account_id,
            "market": req.market.as_market_tag().tag,
            "leverage": req.leverage,
            "interval": req.interval,
            "chartstyle": req.chartstyle,
        },
    )


def add_bot_from_lab(
    executor: SyncExecutor[Authenticated], req: AddBotFromLabRequest
) -> HaasBot:
    """
    Creates new bot from given lab's backtest

    :param executor: Executor for Haas API interaction
    :param req: Details of bot creation
    """
    return executor.execute(
        endpoint="Bot",
        response_type=HaasBot,
        query_params={
            "channel": "ADD_BOT_FROM_LABS",
            "labid": req.lab_id,
            "backtestid": req.backtest_id,
            "botname": req.bot_name,
            "accountid": req.account_id,
            "market": req.market.as_market_tag().tag,
            "leverage": req.leverage,
        },
    )


def delete_bot(executor: SyncExecutor[Authenticated], bot_id: str) -> str:
    return executor.execute(
        endpoint="Bot",
        response_type=str,
        query_params={"channel": "DELETE_BOT", "botid": bot_id},
    )


def get_all_bots(executor: SyncExecutor[Authenticated]) -> list[HaasBot]:
    return executor.execute(
        endpoint="Bot",
        response_type=list[HaasBot],
        query_params={"channel": "GET_BOTS"},
    )


def get_bot(executor: SyncExecutor[Authenticated], bot_id: str) -> HaasBot:
    """
    Retrieves details about a specific bot for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot for which details are requested
    :raises HaasApiError: If bot not found
    :return: Bot details
    """
    return executor.execute(
        endpoint="Bot",
        response_type=HaasBot,
        query_params={"channel": "GET_BOT", "botid": bot_id},
    )


def activate_bot(executor: SyncExecutor[Authenticated], bot_id: str, clean_reports: bool = False) -> bool:
    """
    Activates a specific bot for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot to activate
    :param clean_reports: Whether to clean reports when activating the bot
    :raises HaasApiError: If bot activation fails
    :return: True if activation was successful
    """
    return executor.execute(
        endpoint="Bot",
        response_type=bool,
        query_params={
            "channel": "ACTIVATE_BOT",
            "botid": bot_id,
            "cleanreports": clean_reports,
        },
    )


def deactivate_bot(executor: SyncExecutor[Authenticated], bot_id: str, cancel_orders: bool = False) -> bool:
    """
    Deactivates a specific bot for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot to deactivate
    :param cancel_orders: Whether to cancel open orders when deactivating the bot
    :raises HaasApiError: If bot deactivation fails
    :return: True if deactivation was successful
    """
    return executor.execute(
        endpoint="Bot",
        response_type=bool,
        query_params={
            "channel": "DEACTIVATE_BOT",
            "botid": bot_id,
            "cancelorders": cancel_orders,
        },
    )


def edit_bot_settings(executor: SyncExecutor[Authenticated], bot_id: str, settings: dict) -> HaasBot:
    """
    Edits the settings of a specific bot for an authenticated user.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot to edit
    :param settings: A dictionary containing the settings to update
    :raises HaasApiError: If bot settings update fails
    :return: Updated bot details
    """
    return executor.execute(
        endpoint="Bot",
        response_type=HaasBot,
        query_params={
            "channel": "EDIT_SETTINGS",
            "botid": bot_id,
            "settings": json.dumps(settings),
        },
    )


def get_bot_runtime_report(executor: SyncExecutor[Authenticated], bot_id: str) -> BotRuntimeReport:
    """
    Retrieves the runtime report for a specific bot.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot for which to retrieve the runtime report
    :raises HaasApiError: If retrieval fails
    :return: Bot runtime report
    """
    return executor.execute(
        endpoint="Bot",
        response_type=BotRuntimeReport,
        query_params={
            "channel": "GET_RUNTIME_REPORT",
            "botid": bot_id,
        },
    )


def get_bot_open_orders(executor: SyncExecutor[Authenticated], bot_id: str) -> BotOrderList:
    """
    Retrieves the open orders for a specific bot.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot for which to retrieve the open orders
    :raises HaasApiError: If retrieval fails
    :return: List of open orders for the bot
    """
    return executor.execute(
        endpoint="Bot",
        response_type=BotOrderList,
        query_params={
            "channel": "GET_RUNTIME_OPEN_ORDERS",
            "botid": bot_id,
        },
    )


def get_bot_open_positions(executor: SyncExecutor[Authenticated], bot_id: str) -> BotPositionList:
    """
    Retrieves the open positions for a specific bot.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot for which to retrieve the open positions
    :raises HaasApiError: If retrieval fails
    :return: List of open positions for the bot
    """
    return executor.execute(
        endpoint="Bot",
        response_type=BotPositionList,
        query_params={
            "channel": "GET_RUNTIME_OPEN_POSITIONS",
            "botid": bot_id,
        },
    )


def get_bot_closed_positions(executor: SyncExecutor[Authenticated], bot_id: str, next_page_id: int, page_length: int) -> BotClosedPositionList:
    """
    Retrieves the closed positions for a specific bot.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot for which to retrieve the closed positions
    :param next_page_id: The ID of the next page to retrieve
    :param page_length: The number of items per page
    :raises HaasApiError: If retrieval fails
    :return: Paginated list of closed positions for the bot
    """
    return executor.execute(
        endpoint="Bot",
        response_type=BotClosedPositionList,
        query_params={
            "channel": "GET_RUNTIME_CLOSED_POSITIONS",
            "botid": bot_id,
            "nextpageid": next_page_id,
            "pagelength": page_length,
        },
    )


def reset_bot(executor: SyncExecutor[Authenticated], bot_id: str, config: BotResetConfig) -> bool:
    """
    Resets a specific bot based on the provided configuration.

    :param executor: Executor for Haas API interaction
    :param bot_id: The ID of the bot to reset
    :param config: The configuration for resetting the bot
    :raises HaasApiError: If reset fails
    :return: True if reset was successful
    """
    return executor.execute(
        endpoint="Bot",
        response_type=bool,
        query_params={
            "channel": "RESET_BOT",
            "botid": bot_id,
            "config": config.model_dump_json(),
        },
    )

from typing import Iterator, TypeVar

T = TypeVar('T')

def paginate_results(
    executor: SyncExecutor[Authenticated],
    endpoint: HaasApiEndpoint,
    response_type: Type[PaginatedResponse[T]],
    query_params: dict,
    page_length: int = 100,
) -> Iterator[T]:
    """
    Helper function to paginate through results from an API endpoint.

    :param executor: Executor for Haas API interaction
    :param endpoint: The API endpoint to call
    :param response_type: The expected response type
    :param query_params: The query parameters for the API call
    :param page_length: The number of items per page (default: 100)
    :return: An iterator yielding items from the paginated results
    """
    next_page_id = 0
    while True:
        resp = executor.execute(
            endpoint=endpoint,
            response_type=response_type,
            query_params={**query_params, "nextpageid": next_page_id, "pagelength": page_length},
        )
        yield from resp.items
        if resp.next_page_id == 0:
            break
        next_page_id = resp.next_page_id

def rate_limit(max_calls: int, period: float):
    """
    Decorator to rate limit the execution of a function.

    :param max_calls: The maximum number of calls allowed within the period
    :param period: The time period in seconds
    """
    import time
    from collections import deque

    call_timestamps = deque(maxlen=max_calls)

    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(call_timestamps) == max_calls:
                elapsed_time = time.time() - call_timestamps[0]
                if elapsed_time < period:
                    time.sleep(period - elapsed_time)
            call_timestamps.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

def paginate_results(
    executor: SyncExecutor[Authenticated],
    endpoint: HaasApiEndpoint,
    response_type: Type[PaginatedResponse[T]],
    initial_params: dict[str, Any],
    page_size: int = 100
) -> Iterator[T]:
    """
    A generator that handles pagination for API calls that return paginated results.

    :param executor: Executor for Haas API interaction
    :param endpoint: The API endpoint to call
    :param response_type: The expected response type
    :param initial_params: Initial parameters for the API call
    :param page_size: Number of items per page
    :yields: Items from the paginated results
    :raises HaasApiError: If an API error occurs
    """
    params = initial_params.copy()
    params['pagelength'] = page_size
    params['nextpageid'] = 0

    while True:
        try:
            response = executor.execute(endpoint, response_type, params)
        except HaasApiError as e:
            if 'rate limit exceeded' in str(e).lower():
                raise HaasApiRateLimitError("API rate limit exceeded. Please wait before making more requests.") from e
            elif 'authentication' in str(e).lower():
                raise HaasApiAuthenticationError("Authentication failed. Please check your credentials.") from e
            else:
                raise

        for item in response.items:
            yield item

        if response.next_page_id == 0:
            break

        params['nextpageid'] = response.next_page_id
