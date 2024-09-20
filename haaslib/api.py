from typing import List
from pydantic import BaseModel
from haaslib.model import (
    UserLabDetails, BacktestResult, UserLabRecord, 
    CreateLabRequest, UserAccount, AccountData, AccountBalance,
    AccountOrder, AccountPosition, AccountTrade,
    LabConfig, LabSettings, LabParameter, LabExecutionUpdate
)
from haaslib.executor import BaseExecutor, AuthenticatedExecutor

# Labs API functions

def get_labs(executor: AuthenticatedExecutor) -> List[UserLabRecord]:
    """Returns the saved labs records."""
    return executor.execute(
        endpoint="Labs",
        response_type=List[UserLabRecord],
        query_params={"channel": "GET_LABS"},
    )

def create_lab(executor: AuthenticatedExecutor, request: CreateLabRequest) -> UserLabDetails:
    """Creates a new lab record."""
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "CREATE_LAB",
            "scriptid": request.script_id,
            "name": request.name,
            "accountid": request.account_id,
            "market": request.market,
            "interval": request.interval,
            "style": request.default_price_data_style,
        },
    )

def update_lab_details(
    executor: AuthenticatedExecutor,
    lab_id: str,
    name: str,
    type: int,
    config: LabConfig,
    settings: LabSettings,
    parameters: List[LabParameter]
) -> UserLabDetails:
    """Updates the lab's configuration."""
    return executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "UPDATE_LAB_DETAILS",
            "labid": lab_id,
            "name": name,
            "type": type,
            "config": config.dict(),
            "settings": settings.dict(),
            "parameters": [param.dict() for param in parameters],
        },
    )

def get_lab_execution_update(executor: AuthenticatedExecutor, lab_id: str) -> LabExecutionUpdate:
    """Gets an update on the lab execution."""
    return executor.execute(
        endpoint="Labs",
        response_type=LabExecutionUpdate,
        query_params={
            "channel": "GET_LAB_EXECUTION_UPDATE",
            "labid": lab_id,
        },
    )

# Account API functions

def get_accounts(executor: AuthenticatedExecutor) -> List[UserAccount]:
    return executor.execute(
        endpoint="Account",
        response_type=List[UserAccount],
        query_params={"channel": "GET_ACCOUNTS"},
    )

def get_account_data(executor: AuthenticatedExecutor, account_id: str) -> AccountData:
    return executor.execute(
        endpoint="Account",
        response_type=AccountData,
        query_params={
            "channel": "GET_ACCOUNT_DATA",
            "accountid": account_id,
        },
    )

def get_balance(executor: AuthenticatedExecutor, account_id: str) -> AccountBalance:
    return executor.execute(
        endpoint="Account",
        response_type=AccountBalance,
        query_params={
            "channel": "GET_BALANCE",
            "accountid": account_id,
        },
    )

# Add more functions for other API endpoints...
