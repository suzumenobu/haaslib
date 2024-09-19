from typing import Any, List

from haaslib.api import SyncExecutor, Authenticated
from haaslib.model import ConversionResult, BalanceMutation

class PortfolioAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def convert(self, price_source: str, from_currency: str, to_currency: str, amount: float) -> ConversionResult:
        """
        Converts an amount from one currency to another.

        :param price_source: Name of the price source, like BINANCE
        :param from_currency: Currency to convert from
        :param to_currency: Currency to convert to
        :param amount: Amount to convert
        :raises HaasApiError: If the API call fails
        :return: Conversion result
        """
        return self.executor.execute(
            endpoint="Portfolio",
            response_type=ConversionResult,
            query_params={
                "channel": "CONVERT",
                "pricesource": price_source,
                "fromcurrency": from_currency,
                "tocurrency": to_currency,
                "amount": amount,
            },
        )

    def get_balance_mutations(self, account_ids: List[str], next_page_id: int, page_length: int) -> List[BalanceMutation]:
        """
        Returns the balance mutation per user.

        :param account_ids: List of account IDs
        :param next_page_id: ID of the next page for pagination
        :param page_length: Number of results to return per page
        :raises HaasApiError: If the API call fails
        :return: List of balance mutations
        """
        return self.executor.execute(
            endpoint="Portfolio",
            response_type=List[BalanceMutation],
            query_params={
                "channel": "GET_BALANCE_MUTATIONS",
                "accountids": account_ids,
                "nextpageid": next_page_id,
                "pagelength": page_length,
            },
        )