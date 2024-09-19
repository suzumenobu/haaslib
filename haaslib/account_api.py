from typing import List

from haaslib.api import SyncExecutor, Authenticated
from haaslib.model import UserAccount, AccountData, AccountBalance, AccountOrder, AccountPosition, AccountTrade

class AccountAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def get_accounts(self) -> List[UserAccount]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[UserAccount],
            query_params={"channel": "GET_ACCOUNTS"},
        )

    def get_account_data(self, account_id: str) -> AccountData:
        return self.executor.execute(
            endpoint="Account",
            response_type=AccountData,
            query_params={
                "channel": "GET_ACCOUNT_DATA",
                "accountid": account_id,
            },
        )

    def get_balance(self, account_id: str) -> AccountBalance:
        return self.executor.execute(
            endpoint="Account",
            response_type=AccountBalance,
            query_params={
                "channel": "GET_BALANCE",
                "accountid": account_id,
            },
        )

    def get_all_balances(self) -> List[AccountBalance]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[AccountBalance],
            query_params={"channel": "GET_ALL_BALANCES"},
        )

    def get_orders(self, account_id: str) -> List[AccountOrder]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[AccountOrder],
            query_params={
                "channel": "GET_ORDERS",
                "accountid": account_id,
            },
        )

    def get_all_orders(self) -> List[AccountOrder]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[AccountOrder],
            query_params={"channel": "GET_ALL_ORDERS"},
        )

    def get_positions(self, account_id: str) -> List[AccountPosition]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[AccountPosition],
            query_params={
                "channel": "GET_POSITIONS",
                "accountid": account_id,
            },
        )

    def get_all_positions(self) -> List[AccountPosition]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[AccountPosition],
            query_params={"channel": "GET_ALL_POSITIONS"},
        )

    def get_trades(self, account_ids: List[str], market_search_tags: List[str], next_page_id: int, page_length: int) -> List[AccountTrade]:
        return self.executor.execute(
            endpoint="Account",
            response_type=List[AccountTrade],
            query_params={
                "channel": "GET_TRADES",
                "accountids": account_ids,
                "marketsearchtags": market_search_tags,
                "nextpageid": next_page_id,
                "pagelength": page_length,
            },
        )