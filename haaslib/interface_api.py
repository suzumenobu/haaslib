from typing import Any

from haaslib.api import SyncExecutor, Authenticated
from haaslib.model import MarketInfo, MarketPriceInfo, MarketTAInfo

class InterfaceAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def market_info(self, market: str) -> MarketInfo:
        """
        Returns the market information page.

        :param market: Name of the market, like BINANCE_BTC_USDT_
        :raises HaasApiError: If the API call fails
        :return: Market information
        """
        return self.executor.execute(
            endpoint="Interface",
            response_type=MarketInfo,
            query_params={
                "channel": "MARKET_INFO",
                "market": market,
            },
        )

    def market_price_info(self, market: str) -> MarketPriceInfo:
        """
        Returns the market price information page.

        :param market: Name of the market, like BINANCE_BTC_USDT_
        :raises HaasApiError: If the API call fails
        :return: Market price information
        """
        return self.executor.execute(
            endpoint="Interface",
            response_type=MarketPriceInfo,
            query_params={
                "channel": "MARKET_PRICE_INFO",
                "market": market,
            },
        )

    def market_ta_info(self, market: str) -> MarketTAInfo:
        """
        Returns the market price technical analysis page.

        :param market: Name of the market, like BINANCE_BTC_USDT_
        :raises HaasApiError: If the API call fails
        :return: Market technical analysis information
        """
        return self.executor.execute(
            endpoint="Interface",
            response_type=MarketTAInfo,
            query_params={
                "channel": "MARKET_TA_INFO",
                "market": market,
            },
        )