from typing import List
from ..executor import RequestsExecutor, Authenticated
from ..models.account import UserAccount, AccountData, AccountList
from ..exceptions import AccountError

def get_accounts(executor: RequestsExecutor[Authenticated]) -> List[UserAccount]:
    """Get all user accounts"""
    response = executor.execute(
        endpoint="Account",
        response_type=List[UserAccount],
        query_params={"channel": "GET_ACCOUNTS"}
    )
    
    if not response.Success:
        raise AccountError(f"Failed to get accounts: {response.Error}")
    
    return response.Data or []

def get_account_data(
    executor: RequestsExecutor[Authenticated],
    account_id: str
) -> AccountData:
    """Get detailed account data"""
    response = executor.execute(
        endpoint="Account",
        response_type=AccountData,
        query_params={
            "channel": "GET_ACCOUNT_DATA",
            "accountId": account_id
        }
    )
    
    if not response.Success:
        raise AccountError(f"Failed to get account data: {response.Error}")
    
    return response.Data

def get_account_balances(
    executor: RequestsExecutor[Authenticated],
    account_id: str
) -> AccountList:
    """Get account balances"""
    response = executor.execute(
        endpoint="Account",
        response_type=AccountList,
        query_params={
            "channel": "GET_BALANCES",
            "accountId": account_id
        }
    )
    
    if not response.Success:
        raise AccountError(f"Failed to get account balances: {response.Error}")
    
    return response.Data
