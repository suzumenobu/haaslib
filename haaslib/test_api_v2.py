import sys
import os
import time
import random
import json
from time import sleep
from typing import Literal, List, Dict, Any, Type, TypeVar
import requests
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from .logging_config import logger
from .config import config
from .api import RequestsExecutor, Guest, Authenticated, HaasApiError
from .model import MarketList, AccountList
from .Phyton_automatically_generated.DataModel.MarketInformation import MarketInformation
from typing import Dict, Any, List

# Load environment variables from .env file
load_dotenv()

class HaasApiTest(unittest.TestCase):
    def setUp(self):
        self.executor = RequestsExecutor(host=config.API_HOST, port=config.API_PORT, state=Guest())

    def test_api_accessibility(self):
        logger.info("Testing API accessibility...")
        try:
            response = self.executor.execute(
                endpoint="User",
                response_type=Dict[str, Any],
                query_params={"channel": "PING"}
            )
            self.assertTrue(response.get('Success'), "API should return a success response")
            self.assertEqual(response.get('Data'), 'PONG', "API should return 'PONG' for PING request")
        except HaasApiError as e:
            self.fail(f"Failed to access API: {str(e)}")

    def test_authentication(self):
        logger.info("Testing authentication...")
        try:
            authenticated_executor = self.executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
            self.assertIsInstance(authenticated_executor.state, Authenticated)
            self.assertIsNotNone(authenticated_executor.state.user_id)
            self.assertIsNotNone(authenticated_executor.state.interface_key)
            logger.info("Authentication successful.")
        except HaasApiError as e:
            self.fail(f"Authentication failed: {str(e)}")

    def test_get_accounts(self):
        logger.info("Testing get_accounts...")
        try:
            authenticated_executor = self.executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
            accounts = authenticated_executor.execute(
                endpoint="Account",
                response_type=AccountList,
                query_params={"channel": "GET_ACCOUNTS"}
            )
            self.assertIsInstance(accounts, AccountList)
            self.assertTrue(len(accounts.Data) > 0, "User should have at least one account")
            logger.info(f"Retrieved {len(accounts.Data)} accounts.")
        except HaasApiError as e:
            self.fail(f"Failed to get accounts: {str(e)}")

    def test_get_all_markets(self):
        logger.info("Testing get_all_markets...")
        try:
            authenticated_executor = self.executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
            markets = authenticated_executor.execute(
                endpoint="Price",
                response_type=MarketList,
                query_params={"channel": "MARKETLIST"}
            )
            self.assertIsInstance(markets, MarketList)
            self.assertTrue(len(markets.root) > 0, "There should be at least one market")
            self.assertIsInstance(markets.root[0], MarketInformation)
            logger.info(f"Retrieved {len(markets.root)} markets.")
        except HaasApiError as e:
            self.fail(f"Failed to get markets: {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
