# Import necessary modules
from haaslib.model import (
    CloudMarket,
    UserAccount,
    HaasScriptItemWithDependencies,
    CreateLabRequest,
    StartLabExecutionRequest,
    UserLabDetails,
    GetBacktestResultRequest,
    UserLabBacktestResult,
    UserLabRecord,
    CreateBotRequest,
    AddBotFromLabRequest,
    HaasBot,
    MarketList,
    AccountList,
)
from haaslib.api import SyncExecutor, Authenticated, HaasApiError
from typing import List, Dict, Any
from .logging_config import logger
from .api import HaasApiError
from .Phyton_automatically_generated.DataModel.MarketInformation import MarketInformation

def get_all_markets(executor: SyncExecutor[Authenticated]) -> List[MarketInformation]:
    logger.info("Fetching all markets")
    try:
        response = executor.execute(
            endpoint="Price",
            response_type=MarketList,
            query_params={"channel": "MARKETLIST"}
        )
        return response.root
    except Exception as e:
        logger.error(f"Failed to fetch markets: {str(e)}")
        raise HaasApiError(f"Failed to fetch markets: {str(e)}")

def get_all_markets_by_pricesource(executor: SyncExecutor[Authenticated]) -> Dict[str, List[CloudMarket]]:
    logger.info("Fetching all markets by price source")
    try:
        return executor.execute(
            endpoint="Price",
            response_type=Dict[str, List[CloudMarket]],
            query_params={"channel": "GET_MARKETS_BY_PRICESOURCE"}
        )
    except Exception as e:
        logger.error(f"Failed to fetch markets by price source: {str(e)}")
        raise HaasApiError(f"Failed to fetch markets by price source: {str(e)}")

def get_unique_pricesources(executor: SyncExecutor[Authenticated]) -> List[str]:
    logger.info("Fetching unique price sources")
    try:
        return executor.execute(
            endpoint="Price",
            response_type=List[str],
            query_params={"channel": "GET_UNIQUE_PRICESOURCES"}
        )
    except Exception as e:
        logger.error(f"Failed to fetch unique price sources: {str(e)}")
        raise HaasApiError(f"Failed to fetch unique price sources: {str(e)}")

def get_all_scripts(executor: SyncExecutor[Authenticated]) -> List[HaasScriptItemWithDependencies]:
    logger.info("Fetching all scripts")
    try:
        return executor.execute(
            endpoint="HaasScript",
            response_type=List[HaasScriptItemWithDependencies],
            query_params={"channel": "GET_SCRIPTS"}
        )
    except Exception as e:
        logger.error(f"Failed to fetch scripts: {str(e)}")
        raise HaasApiError(f"Failed to fetch scripts: {str(e)}")

def get_accounts(executor: SyncExecutor[Authenticated]) -> AccountList:
    logger.info("Fetching user accounts")
    try:
        return executor.execute(
            endpoint="Account",
            response_type=AccountList,
            query_params={"channel": "GET_ACCOUNTS"}
        )
    except Exception as e:
        logger.error(f"Failed to fetch accounts: {str(e)}")
        raise HaasApiError(f"Failed to fetch accounts: {str(e)}")

def create_lab(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def start_lab_execution(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def get_lab_details(executor: SyncExecutor[Authenticated], lab_id):
    # Implementation here
    pass

def update_lab_details(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def update_multiple_lab_details(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def get_backtest_result(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def get_all_labs(executor: SyncExecutor[Authenticated]):
    # Implementation here
    pass

def delete_lab(executor: SyncExecutor[Authenticated], lab_id):
    # Implementation here
    pass

def add_bot(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def add_bot_from_lab(executor: SyncExecutor[Authenticated], request):
    # Implementation here
    pass

def delete_bot(executor: SyncExecutor[Authenticated], bot_id):
    # Implementation here
    pass

def get_all_bots(executor: SyncExecutor[Authenticated]):
    # Implementation here
    pass

def get_trading_pairs(executor: SyncExecutor[Authenticated]) -> list[CloudMarket]:
    """
    Fetches all trading pairs (markets) for the given session

    :param executor: Executor for Haas API interaction
    :raises HaasApiError: If the API request fails
    :return: List of all trading pairs (markets)
    """
    return executor.execute(
        endpoint="Price",
        response_type=list[CloudMarket],
        query_params={"channel": "GET_TRADING_PAIRS"},
    )

# Add other functions that are being imported in __init__.py




