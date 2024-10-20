import random
import sys
import traceback
import time

try:
    import requests
except ImportError:
    print("Error: The 'requests' library is not installed. Please install it using 'pip install requests'.")
    sys.exit(1)

try:
    from pydantic import ValidationError
except ImportError:
    print("Error: The 'pydantic' library is not installed. Please install it using 'pip install pydantic'.")
    sys.exit(1)

from haaslib.api import RequestsExecutor, HaasApiError, Guest
from haaslib.model import (
    AuthenticatedSessionResponse,
    CreateLabRequest,
    CreateBotRequest,
    StartLabExecutionRequest,
    CloudMarket,
    HaasScriptItemWithDependencies,
)
from haaslib.domain import MarketTag

def test_authentication(executor):
    print("\n--- Testing authentication ---")
    try:
        executor = executor.authenticate(
            email="garrypotterr@gmail.com", password="IQYTCQJIQYTCQJ"
        )
        print("Authentication successful!")
        print(f"Authenticated state: {executor.state}")
        return executor
    except HaasApiError as e:
        print(f"Authentication failed: {e}")
        raise

def test_get_markets(executor):
    print("\n--- Testing get_all_markets ---")
    try:
        markets = executor.execute(
            endpoint="Price",
            response_type=list,
            query_params={"channel": "MARKETLIST"},
        )
        print(f"Successfully retrieved {len(markets)} markets")
        if markets:
            print(f"Sample market: {markets[0]}")
        return markets
    except HaasApiError as e:
        print(f"Failed to get markets: {e}")

def test_get_scripts(executor):
    print("\n--- Testing get_all_scripts ---")
    try:
        scripts = executor.execute(
            endpoint="HaasScript",
            response_type=list,
            query_params={"channel": "GET_ALL_SCRIPT_ITEMS"},
        )
        print(f"Successfully retrieved {len(scripts)} scripts")
        if scripts:
            print(f"Sample script: {scripts[0]}")
        return scripts
    except HaasApiError as e:
        print(f"Failed to get scripts: {e}")

def test_get_accounts(executor):
    print("\n--- Testing get_accounts ---")
    try:
        accounts = executor.execute(
            endpoint="Account",
            response_type=list,
            query_params={"channel": "GET_ACCOUNTS"},
        )
        print(f"Successfully retrieved {len(accounts)} accounts")
        if accounts:
            print(f"Sample account: {accounts[0]}")
        return accounts
    except HaasApiError as e:
        print(f"Failed to get accounts: {e}")

def test_create_lab(executor, script_id, account_id):
    print("\n--- Testing create_lab ---")
    try:
        req = CreateLabRequest(
            script_id=script_id,
            name=f"Test Lab {int(time.time())}",
            account_id=account_id,
            market=MarketTag("BINANCE_BTC_USDT_SPOT"),
            interval=15,
            default_price_data_style="CandleStick"
        )
        lab = executor.execute(
            endpoint="Labs",
            response_type=dict,
            query_params={
                "channel": "CREATE_LAB",
                "scriptId": req.script_id,
                "name": req.name,
                "accountId": req.account_id,
                "market": req.market.tag,
                "interval": req.interval,
                "style": req.default_price_data_style,
            },
        )
        print(f"Successfully created lab: {lab}")
        return lab
    except HaasApiError as e:
        print(f"Failed to create lab: {e}")

def test_create_bot(executor, script, account_id, market):
    print("\n--- Testing create_bot ---")
    try:
        req = CreateBotRequest(
            bot_name=f"Test Bot {int(time.time())}",
            script=script,
            account_id=account_id,
            market=market,
            leverage=1,
            interval=15,
            chartstyle=301
        )
        bot = executor.execute(
            endpoint="Bot",
            response_type=dict,
            query_params={
                "channel": "ADD_BOT",
                "botname": req.bot_name,
                "scriptid": req.script.id,
                "scripttype": req.script.type,
                "accountid": req.account_id,
                "market": req.market.as_market_tag().tag,
                "leverage": req.leverage,
                "interval": req.interval,
                "chartstyle": req.chartstyle,
            },
        )
        print(f"Successfully created bot: {bot}")
        return bot
    except HaasApiError as e:
        print(f"Failed to create bot: {e}")

def test_start_lab_execution(executor, lab_id):
    print("\n--- Testing start_lab_execution ---")
    try:
        current_time = int(time.time())
        req = StartLabExecutionRequest(
            lab_id=lab_id,
            start_unix=current_time - 86400,  # 24 hours ago
            end_unix=current_time,
            send_email=False
        )
        result = executor.execute(
            endpoint="Labs",
            response_type=dict,
            query_params={
                "channel": "START_LAB_EXECUTION",
                "labid": req.lab_id,
                "startunix": req.start_unix,
                "endunix": req.end_unix,
                "sendemail": req.send_email,
            },
        )
        print(f"Successfully started lab execution: {result}")
        return result
    except HaasApiError as e:
        print(f"Failed to start lab execution: {e}")

def test_invalid_credentials(executor):
    print("\n--- Testing invalid credentials ---")
    try:
        invalid_email = f"invalid_{random.randint(1000, 9999)}@example.com"
        invalid_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
        
        result = executor.authenticate(
            email=invalid_email, password=invalid_password
        )
        print(f"Warning: Authentication succeeded with invalid credentials.")
        print(f"Authenticated state: {result.state}")
        print("This might indicate an issue with the API's credential validation.")
        return False
    except HaasApiError as e:
        print(f"Authentication failed as expected: {e}")
        return True
    except Exception as e:
        print(f"Unexpected error during invalid credential test: {e}")
        return False

def main():
    try:
        executor = RequestsExecutor(host="127.0.0.1", port=8090, state=Guest())
        
        # Test valid authentication
        executor = test_authentication(executor)
        
        # Test invalid credentials
        invalid_cred_test_passed = test_invalid_credentials(RequestsExecutor(host="127.0.0.1", port=8090, state=Guest()))
        if not invalid_cred_test_passed:
            print("Warning: The API accepted invalid credentials. This might be a security issue.")
        
        # Test other API endpoints
        markets = test_get_markets(executor)
        scripts = test_get_scripts(executor)
        accounts = test_get_accounts(executor)

        if scripts and accounts and markets:
            # Create a lab
            lab = test_create_lab(executor, scripts[0]['SID'], accounts[0]['AID'])
            
            # Create a bot
            bot = test_create_bot(executor, 
                                  HaasScriptItemWithDependencies(**scripts[0]), 
                                  accounts[0]['AID'], 
                                  CloudMarket(**markets[0]))

            # Start lab execution
            if lab:
                test_start_lab_execution(executor, lab['LID'])

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("Exception details:")
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            print(line, end="")

if __name__ == "__main__":
    main()
