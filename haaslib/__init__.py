from .logging_config import setup_logging, logger

setup_logging()

logger.info("Starting import in __init__.py")

try:
    from .api import RequestsExecutor, HaasApiError, Guest, Authenticated
    print("Successfully imported RequestsExecutor and other API components")
except ImportError as e:
    print(f"Error importing API components: {e}")

print("Continuing with other imports")

# Import each function individually
imported_functions = []
function_names = [
    'get_all_markets',
    'get_all_markets_by_pricesource',
    'get_unique_pricesources',
    'get_all_scripts',
    'get_accounts',
    'create_lab',
    'start_lab_execution',
    'get_lab_details',
    'update_lab_details',
    'update_multiple_lab_details',
    'get_backtest_result',
    'get_all_labs',
    'delete_lab',
    'add_bot',
    'add_bot_from_lab',
    'delete_bot',
    'get_all_bots',
    'get_trading_pairs',
]

for func in function_names:
    try:
        exec(f"from .api_functions import {func}")
        imported_functions.append(func)
        print(f"Successfully imported {func}")
    except ImportError as e:
        print(f"Error importing {func}: {e}")

print("Finished imports in __init__.py")

__all__ = [
    'HaasApiError',
    'RequestsExecutor',
    'Guest',
    'Authenticated',
] + imported_functions

print(f"__all__ contents: {__all__}")

# Make imported functions available at the module level
for func in imported_functions:
    locals()[func] = eval(func)
