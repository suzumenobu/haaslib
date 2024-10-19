import time
from haaslib.examples import AccountAPI, PriceAPI
from haaslib.examples.config import config
from haaslib.executor import AuthenticatedExecutor
from haaslib.api import get_all_markets_by_pricesource
from loguru import logger

def main():
    executor = AuthenticatedExecutor(
        host=config.get("API_HOST"),
        port=config.get("API_PORT"),
        protocol=config.get("API_PROTOCOL"),
        email="garrypotterr@gmail.com",
        password="IQYTCQJIQYTCQJ",
    )

    account_api = AccountAPI(executor)
    price_api = PriceAPI(executor)

    try:
        accounts = account_api.get_accounts()
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

            # Get markets for the selected account's price source
            try:
                account_data = account_api.get_account_data(selected_account_id)
                if account_data and hasattr(account_data, 'price_source'):
                    price_source = account_data.price_source
                    markets = get_all_markets_by_pricesource(executor, price_source)
                    logger.info("\nAvailable Markets for selected account:")
                    if markets:
                        for market in markets:
                            logger.info(f"- {market.price_source} ({market.primary}/{market.secondary})")
                    else:
                        logger.warning(f"No markets found for price source: {price_source}")
                else:
                    logger.error("Could not retrieve account data or price source.")

                # Get account balance
                balance = account_api.get_balance(selected_account_id)
                logger.info(f"\nAccount Balance: {balance}")

            except Exception as e:
                logger.exception(f"Error retrieving markets or balance for account {selected_account_id}: {e}")

        else:
            logger.warning("No accounts found.")

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
