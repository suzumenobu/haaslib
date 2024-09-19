from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    price_api = api.PriceAPI(executor)

    # Get all markets
    markets = price_api.market_list()
    print(f"Total markets: {len(markets)}")

    # Get price for a specific market
    market = "BINANCE_BTC_USDT_SPOT"
    price = price_api.price(market)
    print(f"Current price for {market}: {price.price}")

    # Get orderbook for a specific market
    orderbook = price_api.orderbook(market)
    print(f"Top bid: {orderbook.bids[0]}")
    print(f"Top ask: {orderbook.asks[0]}")

    # Get last trades for a specific market
    last_trades = price_api.last_trades(market)
    print(f"Last trade: {last_trades[0]}")

    # Get ticks for a specific market
    ticks = price_api.last_ticks(market, interval=15)
    print(f"Last tick: {ticks[-1]}")

if __name__ == "__main__":
    main()