from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    portfolio_api = api.PortfolioAPI(executor)

    # Convert currency
    conversion = portfolio_api.convert(
        price_source="BINANCE",
        from_currency="BTC",
        to_currency="USDT",
        amount=1.0
    )
    print(f"1 BTC is worth {conversion.converted_amount} USDT")

    # Get balance mutations
    account_ids = ["account_id_1", "account_id_2"]  # Replace with actual account IDs
    mutations = portfolio_api.get_balance_mutations(account_ids, next_page_id=0, page_length=100)
    print("Recent balance mutations:")
    for mutation in mutations:
        print(f"Account: {mutation.account_id}, Amount: {mutation.amount} {mutation.currency}")

if __name__ == "__main__":
    main()