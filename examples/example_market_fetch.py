import random
import logging
# Update imports to use executor instead of api
from haaslib.executor import RequestsExecutor, Guest, HaasApiError
from haaslib.api import get_accounts  # Keep this import as it's still in api.py
from haaslib.config import config
from haaslib.models.market import Market

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Create a RequestsExecutor instance
    executor = RequestsExecutor(
        host=config.API_HOST,
        port=config.API_PORT,
        state=Guest()
    )

    try:
        # Authenticate
        logger.info("Authenticating...")
        logger.debug(f"Using email: {config.API_EMAIL}")
        logger.debug(f"Using password: {'*' * len(config.API_PASSWORD)}")
        
        authenticated_executor = executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
        logger.info("Authentication successful.")
        logger.debug(f"Authenticated executor state: {authenticated_executor.state}")

        # Get accounts
        logger.info("Fetching accounts...")
        accounts_response = get_accounts(authenticated_executor)
        
        # Update to handle the new response structure
        if not accounts_response.Success:
            logger.error(f"Failed to fetch accounts: {accounts_response.Error}")
            return
            
        accounts = accounts_response.Data
        logger.info(f"Found {len(accounts)} accounts.")

        if not accounts:
            logger.error("No accounts found.")
            return

        random_account = random.choice(accounts)
        logger.info(f"Selected random account: {random_account.AccountId}")  # Update to match your actual account model

        # Get all markets for Binance
        logger.info("Fetching all markets for Binance...")
        try:
            markets = get_all_markets_by_pricesource(authenticated_executor, "binance")
            logger.info(f"Total number of Binance markets: {len(markets)}")

            # Print details of the first market
            if markets:
                first_market = markets[0]
                logger.info("First market details:")
                logger.info(f"  Symbol: {first_market.symbol}")
                logger.info(f"  Price Source: {first_market.price_source}")
                logger.info(f"  Asset: {first_market.asset}")
                logger.info(f"  Currency: {first_market.currency}")
            else:
                logger.warning("No markets found for Binance.")
        except HaasApiError as e:
            logger.error(f"Failed to fetch markets: {e}")

    except HaasApiError as e:
        logger.error(f"An API error occurred: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
