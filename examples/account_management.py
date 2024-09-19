from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    account_api = api.AccountAPI(executor)

    # Get all accounts
    accounts = account_api.get_accounts()
    print(f"Total accounts: {len(accounts)}")

    if accounts:
        account = accounts[0]
        print(f"Working with account: {account.name}")

        # Get account data
        account_data = account_api.get_account_data(account.account_id)
        print(f"Account data: {account_data}")

        # Get balance
        balance = account_api.get_balance(account.account_id)
        print(f"Account balance: {balance}")

        # Get orders
        orders = account_api.get_orders(account.account_id)
        print(f"Open orders: {len(orders)}")

        # Get positions
        positions = account_api.get_positions(account.account_id)
        print(f"Open positions: {len(positions)}")

if __name__ == "__main__":
    main()