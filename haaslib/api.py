from __future__ import annotations

import copy
import dataclasses
import json
import random
import sys
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
    List,
    Dict,
    Union,
)
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from pydantic import BaseModel, TypeAdapter, ValidationError, RootModel, Field
from pydantic.json import pydantic_encoder

from .model import (
    AddBotFromLabRequest,
    ApiResponse,
    AuthenticatedSessionResponse,
    AuthenticatedSessionResponseData,
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
    LicenseDetails,
    LoginResponse,
    Market,
    MarketList,
    Account,
    AccountList,
)
from .config import config

ApiResponseData = TypeVar(
    "ApiResponseData", bound=BaseModel | Collection[BaseModel] | bool | str
)
"""Any response from Haas API should be `pydantic` model or collection of them."""

HaasApiEndpoint = Literal["Labs", "Account", "HaasScript", "Price", "User", "Bot"]
"""Known Haas API endpoints"""


class HaaslibException(Exception):
    """Base exception for haaslib."""
    pass


class HaasApiError(HaaslibException):
    """Exception raised for errors in the API."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BaseState(ABC):
    pass


@dataclass
class Guest(BaseState):
    pass


@dataclass
class Authenticated(BaseState):
    user_id: str
    interface_key: str


S = TypeVar('S', bound=BaseState)


class SyncExecutor(Generic[S]):
    """
    Main protocol for interaction with HaasAPI.
    """

    def __init__(self, state: S):
        self.state = state

    @abstractmethod
    def execute(self, endpoint: HaasApiEndpoint, response_type: Type[ApiResponseData], query_params: Optional[dict] = None) -> ApiResponseData:
        pass

    @abstractmethod
    def authenticate(self, email: str, password: str) -> 'SyncExecutor[Authenticated]':
        pass


@dataclass(kw_only=True, frozen=True, slots=True)
class RequestsExecutor(SyncExecutor[BaseState]):
    """First implementation of `SyncExecutor` based on `requests` library."""

    host: str
    """ Address of the Haas API."""

    port: int
    """ Port of the Haas API."""

    def authenticate(self, email: str, password: str) -> 'RequestsExecutor[Authenticated]':
        interface_key = "".join(f"{random.randint(0, 100)}" for _ in range(10))
        
        # First step: LOGIN_WITH_CREDENTIALS
        credentials_response = self._execute_guest(
            endpoint="User",
            response_type=ApiResponse[dict],
            query_params={
                "channel": "LOGIN_WITH_CREDENTIALS",
                "email": email,
                "password": password,
                "interfaceKey": interface_key,
            }
        )
        
        if not credentials_response.Success:
            raise HaasApiError(f"Login with credentials failed: {credentials_response.Error}")
        
        # Second step: LOGIN_WITH_ONE_TIME_CODE
        otp_response = self._execute_guest(
            endpoint="User",
            response_type=LoginResponse,
            query_params={
                "channel": "LOGIN_WITH_ONE_TIME_CODE",
                "email": email,
                "pincode": random.randint(100_000, 200_000),
                "interfaceKey": interface_key,
            }
        )
        
        if not otp_response.Success or otp_response.Error:
            raise HaasApiError(f"Login with one-time code failed: {otp_response.Error}")
        
        # Add this debug print
        print(f"OTP Response: {otp_response}")
        
        if otp_response.Data is None or not isinstance(otp_response.Data, AuthenticatedSessionResponse):
            raise HaasApiError(f"Unexpected response format: {otp_response}")
        
        return RequestsExecutor(
            host=self.host,
            port=self.port,
            state=Authenticated(
                user_id=otp_response.Data.D.UserId,
                interface_key=interface_key
            )
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
        resp = self._execute_authenticated(endpoint, response_type, query_params)
        
        if isinstance(resp, dict) and 'Success' in resp:
            if not resp['Success']:
                raise HaasApiError(f"API returned error: {resp.get('Error', 'Unknown error')}")
            return resp['Data']
        return resp

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

        if isinstance(self.state, Authenticated):
            query_params["userid"] = self.state.user_id
            query_params["interfacekey"] = self.state.interface_key

        return self._execute_inner(endpoint, response_type, query_params)

    def _execute_guest(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[ApiResponseData],
        query_params: Optional[dict] = None,
    ) -> ApiResponse[ApiResponseData]:
        if query_params is None:
            query_params = {}
        return self._execute_inner(endpoint, response_type, query_params)

    def _execute_inner(
        self,
        endpoint: HaasApiEndpoint,
        response_type: Type[T],
        query_params: Optional[dict] = None,
    ) -> T:
        url = f"{self.protocol}://{self.host}:{self.port}/{endpoint}API.php"
        log.debug(
            f"[{self.state.__class__.__name__}]: Requesting {url=} with {query_params=}"
        )
        try:
            resp = requests.get(url, params=query_params)
            resp.raise_for_status()
            raw_response = resp.json()
            
            print(f"Raw API response: {raw_response}")  # Keep this line for debugging

            if isinstance(response_type, type) and issubclass(response_type, BaseModel):
                try:
                    validated_response = response_type.model_validate(raw_response)
                except ValidationError as e:
                    raise HaasApiException(f"Response validation failed: {e}")
            elif response_type == List[Dict[str, Any]]:
                validated_response = raw_response  # No validation for List[Dict[str, Any]]
            else:
                raise HaasApiException(f"Unsupported response type: {response_type}")

            return validated_response
        except requests.RequestException as e:
            log.error(f"Failed to request: {e}")
            raise HaasApiError(f"Failed to request {endpoint} endpoint: {e}\nURL: {url}\nParams: {query_params}")
        except ValidationError as e:
            log.error(f"Failed to validate response: {raw_response}")
            raise HaasApiError(f"Failed to validate {endpoint}API response: {e}")

    @staticmethod
    def _custom_encoder(**kwargs):
        def base_encoder(obj):
            if isinstance(obj, BaseModel):
                return obj.model_dump(**kwargs)
            else:
                return pydantic_encoder(obj)

        return base_encoder


def get_all_markets(executor: AuthenticatedExecutor) -> MarketList:
    print("Debug: Entering get_all_markets")
    markets = executor.execute(
        endpoint="Price",
        response_type=MarketList,
        query_params={"channel": "MARKETLIST"}
    )
    print(f"Debug: get_all_markets received {len(markets.root)} markets")
    print("Debug: Exiting get_all_markets")
    return markets

def get_accounts(executor: AuthenticatedExecutor) -> AccountList:
    print("Debug: Entering get_accounts")
    accounts = executor.execute(
        endpoint="Account",
        response_type=AccountList,
        query_params={"channel": "GET_ACCOUNTS"}
    )
    print(f"Debug: get_accounts received {len(accounts.Data)} accounts")
    print("Debug: Exiting get_accounts")
    return accounts

def get_all_markets_by_pricesource(
    executor: AuthenticatedExecutor, price_source: str
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


def create_lab(
    executor: SyncExecutor[Authenticated], req: CreateLabRequest
) -> UserLabDetails:
    response = executor.execute(
        endpoint="Labs",
        response_type=dict,  # Change this to dict to handle both success and error cases
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
    
    if not response.get('Success'):
        raise HaasApiError(f"Failed to create lab: {response.get('Error')}")
    
    return UserLabDetails(**response.get('Data', {}))


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


def delete_bot(executor: SyncExecutor[Authenticated], bot_id: str):
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


































































