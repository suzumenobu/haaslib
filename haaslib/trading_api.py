from typing import Any

from haaslib.api import SyncExecutor, Authenticated

class TradingAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def place_order(self, order: Any) -> Any:
        """
        Places an order.

        :param order: The order details
        :return: Response from the API
        """
        return self.executor.execute(
            endpoint="Trading",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "PLACE_ORDER",
                "order": order,
            },
        )

    def cancel_order(self, account_id: str, order_id: str) -> Any:
        """
        Cancels an open order.

        :param account_id: The account ID
        :param order_id: The order ID to cancel
        :return: Response from the API
        """
        return self.executor.execute(
            endpoint="Trading",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "CANCEL_ORDER",
                "accountid": account_id,
                "orderid": order_id,
            },
        )

    def used_margin(self, driver_name: str, driver_type: str, market: str, leverage: float, price: float, amount: float) -> Any:
        """
        Returns what the used margin is.

        :param driver_name: Name of the driver
        :param driver_type: Type of the driver
        :param market: Name of the market, like BINANCE_BTC_USDT_
        :param leverage: Leverage amount
        :param price: Price
        :param amount: Amount
        :return: Used margin information
        """
        return self.executor.execute(
            endpoint="Trading",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "USED_MARGIN",
                "drivername": driver_name,
                "drivertype": driver_type,
                "market": market,
                "leverage": leverage,
                "price": price,
                "amount": amount,
            },
        )

    def max_amount(self, account_id: str, market: str, price: float, used_amount: float, amount_percentage: float, is_buy: bool) -> Any:
        """
        Calculates the maximum trade amount, price and margin.

        :param account_id: The account ID
        :param market: Name of the market, like BINANCE_BTC_USDT_
        :param price: Price
        :param used_amount: Used amount
        :param amount_percentage: Amount percentage
        :param is_buy: Whether it's a buy order
        :return: Maximum amount information
        """
        return self.executor.execute(
            endpoint="Trading",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "MAX_AMOUNT",
                "accountid": account_id,
                "market": market,
                "price": price,
                "usedamount": used_amount,
                "amountpercentage": amount_percentage,
                "isbuy": is_buy,
            },
        )

    def cancel_all_open_orders(self, account_id: str = None, market: str = None) -> Any:
        """
        Cancels all open orders, accountid and market as optional.

        :param account_id: The account ID (optional)
        :param market: Name of the market, like BINANCE_BTC_USDT_ (optional)
        :return: Response from the API
        """
        params = {"channel": "CANCEL_ALL_OPEN_ORDERS"}
        if account_id:
            params["accountid"] = account_id
        if market:
            params["market"] = market
        return self.executor.execute(
            endpoint="Trading",
            response_type=Any,  # Replace with a more specific type if known
            query_params=params,
        )