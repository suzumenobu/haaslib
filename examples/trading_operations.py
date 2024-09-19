from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    trading_api = api.TradingAPI(executor)

    # Place an order
    order = {
        "accountId": "your_account_id",
        "market": "BINANCE_BTC_USDT_SPOT",
        "orderType": "LIMIT",
        "side": "BUY",
        "amount": 0.001,
        "price": 30000,
    }
    result = trading_api.place_order(order)
    print(f"Order placed: {result}")

    # Calculate used margin
    used_margin = trading_api.used_margin(
        driver_name="BINANCE",
        driver_type="SPOT",
        market="BINANCE_BTC_USDT_SPOT",
        leverage=1,
        price=30000,
        amount=0.001
    )
    print(f"Used margin: {used_margin}")

    # Calculate maximum trade amount
    max_amount = trading_api.max_amount(
        account_id="your_account_id",
        market="BINANCE_BTC_USDT_SPOT",
        price=30000,
        used_amount=0,
        amount_percentage=100,
        is_buy=True
    )
    print(f"Maximum trade amount: {max_amount}")

if __name__ == "__main__":
    main()