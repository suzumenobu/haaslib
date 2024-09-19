from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    custom_api = api.CustomAPI(executor)

    # Get default commands
    driver_code = "BINANCE"
    market_tag = "BINANCE_BTC_USDT_SPOT"
    default_commands = custom_api.get_default_commands(driver_code, market_tag)
    print(f"Default commands for {driver_code} on {market_tag}:")
    for command in default_commands:
        print(f"- {command}")

if __name__ == "__main__":
    main()