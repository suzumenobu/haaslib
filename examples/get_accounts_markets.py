import time
from haaslib import api
from loguru import logger

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="garrypotterr@gmail.com", password="IQYTCQJIQYTCQJ")

    try:
        accounts = api.get_accounts(executor)
        logger.info("Available Accounts:")
        for i, account in enumerate(accounts):
            logger.info(f"{i+1}. {account.account_id} ({account.name})")

        if accounts:
            while True:
                try:
                    selected_index = int(input("\nSelect an account (enter number): ")) - 1
                    if 0 <= selected_index < len(accounts):
                        selected_account_id = accounts[selected_index].account_id
                        break
                    else:
                        logger.error("Invalid account number.")
                except ValueError:
                    logger.error("Invalid input. Please enter a number.")

            logger.info(f"\nSelected account: {selected_account_id}")
            markets = api.get_all_markets(executor) # Note: get_all_markets does NOT require an account ID
            logger.info("\nAvailable Markets (Note: This command does not use the selected account):")
            for market in markets:
                logger.info(f"- {market.price_source} ({market.primary}/{market.secondary})")
        else:
            logger.warning("No accounts found.")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
