from typing import List, Dict

from haaslib.api import SyncExecutor, Authenticated
from haaslib.model import PriceSource, Market, Coin, Price, OrderBook, Trade, Tick, FiatConversion

class PriceAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def time(self) -> int:
        return self.executor.execute(
            endpoint="Price",
            response_type=int,
            query_params={"channel": "TIME"},
        )

    def all_price_sources(self) -> List[str]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[str],
            query_params={"channel": "ALL_PRICESOURCES"},
        )

    def price_sources(self) -> List[PriceSource]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[PriceSource],
            query_params={"channel": "PRICESOURCES"},
        )

    def all_markets(self) -> Dict[str, List[Market]]:
        return self.executor.execute(
            endpoint="Price",
            response_type=Dict[str, List[Market]],
            query_params={"channel": "ALL_MARKETS"},
        )

    def market_list(self) -> List[Market]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Market],
            query_params={"channel": "MARKETLIST"},
        )

    def unique_market_list(self) -> List[Market]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Market],
            query_params={"channel": "UNIQUE_MARKETLIST"},
        )

    def markets(self, price_source: str) -> List[Market]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Market],
            query_params={
                "channel": "MARKETS",
                "pricesource": price_source,
            },
        )

    def trade_markets(self, price_source: str) -> List[Market]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Market],
            query_params={
                "channel": "TRADE_MARKETS",
                "pricesource": price_source,
            },
        )

    def coin_list(self) -> List[Coin]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Coin],
            query_params={"channel": "COINLIST"},
        )

    def price(self, market: str) -> Price:
        return self.executor.execute(
            endpoint="Price",
            response_type=Price,
            query_params={
                "channel": "PRICE",
                "market": market,
            },
        )

    def orderbook(self, market: str) -> OrderBook:
        return self.executor.execute(
            endpoint="Price",
            response_type=OrderBook,
            query_params={
                "channel": "ORDERBOOK",
                "market": market,
            },
        )

    def last_trades(self, market: str) -> List[Trade]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Trade],
            query_params={
                "channel": "LASTTRADES",
                "market": market,
            },
        )

    def sync_ticks(self, market: str) -> List[Tick]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Tick],
            query_params={
                "channel": "SYNCTICKS",
                "market": market,
            },
        )

    def last_ticks(self, market: str, interval: int) -> List[Tick]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Tick],
            query_params={
                "channel": "LASTTICKS",
                "market": market,
                "interval": interval,
            },
        )

    def deep_ticks(self, market: str) -> List[Tick]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[Tick],
            query_params={
                "channel": "DEEPTICKS",
                "market": market,
            },
        )

    def snapshot(self, price_source: str) -> Dict[str, Price]:
        return self.executor.execute(
            endpoint="Price",
            response_type=Dict[str, Price],
            query_params={
                "channel": "SNAPSHOT",
                "pricesource": price_source,
            },
        )

    def fiat_conversions(self) -> List[FiatConversion]:
        return self.executor.execute(
            endpoint="Price",
            response_type=List[FiatConversion],
            query_params={"channel": "FIAT_CONVERSIONS"},
        )