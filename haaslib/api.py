from __future__ import annotations

import copy
import dataclasses
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

import pydantic
import requests
from pydantic import BaseModel, TypeAdapter

from haaslib.domain import HaaslibExcpetion
from haaslib.logger import log
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
    UserLabRecord,
)

ApiResponseData = TypeVar(
    "ApiResponseData", bound=BaseModel | Collection[BaseModel] | bool
)
"""Any response from Haas API should be `pydantic` model or collection of them."""

HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User"]
"""Known Haas API endpoints"""


class HaasApiError(HaaslibExcpetion):
    """
    Base Excpetion for haaslib.
    """

    pass


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
        resp = requests.get(url, params=query_params)

        ta = TypeAdapter(ApiResponse[response_type])
        return ta.validate_python(resp.json())


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
        response_type=list[UserLabRecord],
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
