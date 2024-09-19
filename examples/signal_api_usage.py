from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    signal_api = api.SignalAPI(executor)

    # Store a signal
    signal_data = {
        "market": "BINANCE_BTC_USDT_SPOT",
        "action": "BUY",
        "price": 30000,
        "timestamp": 1625097600,
    }
    result = signal_api.store_signal("your_signal_id", "your_secret", signal_data)
    print(f"Signal stored: {result}")

    # Get all signals
    my_signals = signal_api.my_signals()
    print("My signals:")
    for signal in my_signals:
        print(f"Signal ID: {signal['id']}, Market: {signal['market']}, Action: {signal['action']}")

if __name__ == "__main__":
    main()