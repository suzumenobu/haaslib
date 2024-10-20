import sys
import os
import time

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from typing import Literal, List, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from haaslib.api import (
    RequestsExecutor, get_all_markets, get_accounts, HaasApiError, Guest, Authenticated,
    create_lab, start_lab_execution, get_lab_details
)
from haaslib.model import (
    CloudMarket, UserAccount, CreateLabRequest, StartLabExecutionRequest, UserLabDetails, MarketTag
)
from haaslib.domain import PriceDataStyle

def print_and_pause(func_name):
    print(f"\n{'='*40}")
    print(f"Executing: {func_name}")
    print(f"{'='*40}\n")
    time.sleep(2)  # Pause for 2 seconds

class HaasApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.host = os.getenv('HAAS_API_HOST')
        cls.port = int(os.getenv('HAAS_API_PORT', '8090'))
        cls.email = os.getenv('HAAS_API_EMAIL')
        cls.password = os.getenv('HAAS_API_PASSWORD')
        cls.executor = RequestsExecutor(host=cls.host, port=cls.port, state=Guest())

    def test_authentication(self):
        print_and_pause("test_authentication")
        print(f"Attempting authentication for {self.email}...")
        authenticated_executor = self.executor.authenticate(email=self.email, password=self.password)
        self.assertIsInstance(authenticated_executor, RequestsExecutor)
        self.assertIsInstance(authenticated_executor.state, Authenticated)
        print("Authentication successful.")

    def test_get_markets(self):
        print_and_pause("test_get_markets")
        authenticated_executor = self.get_authenticated_executor()
        
        print("Debug: Before calling get_all_markets")
        try:
            markets = get_all_markets(authenticated_executor)
            print("Debug: After calling get_all_markets")
            print(f"Debug: Type of markets: {type(markets)}")
            print(f"Debug: Length of markets: {len(markets)}")
            
            self.assertIsInstance(markets, list)
            self.assertTrue(len(markets) > 0)
            
            print(f"\nNumber of markets: {len(markets)}")
            
            if markets:
                first_market = markets[0]
                self.assertIsInstance(first_market, dict)
                self.assertTrue(len(first_market) > 0)
                print(f"Example market keys: {', '.join(first_market.keys())}")
            
            print("Debug: End of test_get_markets")
        except Exception as e:
            print(f"Debug: Exception occurred in test_get_markets: {str(e)}")
            raise

    def test_get_accounts(self):
        print_and_pause("test_get_accounts")
        authenticated_executor = self.get_authenticated_executor()
        
        print("Debug: Before calling get_accounts")
        try:
            accounts = get_accounts(authenticated_executor)
            print("Debug: After calling get_accounts")
            print(f"Debug: Type of accounts: {type(accounts)}")
            print(f"Debug: Length of accounts: {len(accounts)}")
            
            self.assertIsInstance(accounts, list)
            
            print(f"\nNumber of accounts: {len(accounts)}")
            
            if accounts:
                first_account = accounts[0]
                self.assertIsInstance(first_account, dict)
                print(f"Example account keys: {', '.join(first_account.keys())}")
                print(f"First account: {first_account}")  # Print the first account for inspection
            else:
                print("No accounts found.")
            
            print("Debug: End of test_get_accounts")
        except Exception as e:
            print(f"Debug: Exception occurred in test_get_accounts: {str(e)}")
            raise

    def get_authenticated_executor(self):
        return self.executor.authenticate(email=self.email, password=self.password)

    def test_create_lab(self):
        print_and_pause("test_create_lab")
        authenticated_executor = self.get_authenticated_executor()
        
        print("Debug: Before creating CreateLabRequest")
        create_lab_request = CreateLabRequest(
            script_id="some_script_id",  # Replace with a valid script ID
            name="Test Lab",
            account_id="some_account_id",  # Replace with a valid account ID
            market=MarketTag("BINANCE_BTC_USDT_SPOT"),  # Replace with a valid market tag
            interval=15,
            default_price_data_style="CandleStick"  # Changed this line
        )
        print("Debug: CreateLabRequest created")

        print("Debug: Before calling create_lab")
        try:
            lab_details = create_lab(authenticated_executor, create_lab_request)
            self.assertIsInstance(lab_details, UserLabDetails)
            self.assertTrue(hasattr(lab_details, 'lab_id'), "UserLabDetails should have a lab_id attribute")
            print(f"\nCreated lab with ID: {lab_details.lab_id}")
            print(f"Lab name: {lab_details.name}")
            print(f"Lab script ID: {lab_details.script_id}")
            
            print("Debug: End of test_create_lab")
        except HaasApiError as e:
            self.fail(f"Failed to create lab: {str(e)}")

    def test_lab_interaction(self):
        print_and_pause("test_lab_interaction")
        authenticated_executor = self.get_authenticated_executor()

        # 1. Create a lab
        print("Creating a lab...")
        create_lab_request = CreateLabRequest(
            script_id="example_script_id",
            name="Test Lab",
            account_id="example_account_id",
            market=MarketTag("BINANCE_BTC_USDT_SPOT"),
            interval=15,
            default_price_data_style="CandleStick"  # Changed this line
        )

        try:
            lab_details = create_lab(authenticated_executor, create_lab_request)
            self.assertIsInstance(lab_details, UserLabDetails)
            self.assertTrue(hasattr(lab_details, 'lab_id'), "UserLabDetails should have a lab_id attribute")
            print(f"Created lab with ID: {lab_details.lab_id}")

            # 2. Start lab execution
            print("Starting lab execution...")
            start_execution_request = StartLabExecutionRequest(
                lab_id=lab_details.lab_id,
                start_unix=int(time.time()),
                end_unix=int(time.time()) + 3600,  # 1 hour later
                send_email=False
            )
            started_lab = start_lab_execution(authenticated_executor, start_execution_request)
            self.assertIsInstance(started_lab, UserLabDetails)
            print(f"Started lab execution for lab ID: {started_lab.lab_id}")

            # 3. Get lab details
            print("Getting lab details...")
            retrieved_lab = get_lab_details(authenticated_executor, lab_details.lab_id)
            self.assertIsInstance(retrieved_lab, UserLabDetails)
            self.assertEqual(retrieved_lab.lab_id, lab_details.lab_id)
            print(f"Retrieved details for lab ID: {retrieved_lab.lab_id}")

        except HaasApiError as e:
            self.fail(f"Failed to create lab: {str(e)}")

        print("Lab interaction test completed successfully.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
