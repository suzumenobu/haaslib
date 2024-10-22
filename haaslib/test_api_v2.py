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
from .executor import RequestsExecutor, get_all_markets_by_pricesource, HaasApiError, Guest, Authenticated
from .model import CloudMarket

# Load environment variables from .env file
load_dotenv()

class HaasApiTest(unittest.TestCase):
    def setUp(self):
        self.executor = RequestsExecutor(host=config.API_HOST, port=config.API_PORT, state=Guest())

    def test_api_accessibility(self):
        try:
            response = self.executor.execute(
                endpoint="User",
                response_type=dict,
                query_params={"channel": "PING"}
            )
            self.assertIsInstance(response, dict)
            self.assertTrue(response.get('Success', False), "API should be accessible")
        except HaasApiError as e:
            self.fail(f"API is not accessible: {str(e)}")

    def test_authentication(self):
        try:
            authenticated_executor = self.executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
            self.assertIsInstance(authenticated_executor.state, Authenticated)
        except HaasApiError as e:
            self.fail(f"Authentication failed: {str(e)}")

    def test_get_accounts(self):
        try:
            authenticated_executor = self.executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
            response = authenticated_executor.execute(
                endpoint="Account",
                response_type=dict,
                query_params={"channel": "GET_ACCOUNTS"}
            )
            self.assertIsInstance(response, dict)
            self.assertTrue(response.get('Success', False))
            self.assertTrue(len(response.get('Data', [])) > 0, "User should have at least one account")
        except HaasApiError as e:
            self.fail(f"Failed to get accounts: {str(e)}")

    def test_get_all_markets(self):
        try:
            authenticated_executor = self.executor.authenticate(email=config.API_EMAIL, password=config.API_PASSWORD)
            markets = get_all_markets_by_pricesource(authenticated_executor, "binance")
            self.assertIsInstance(markets, list)
            self.assertTrue(len(markets) > 0, "There should be at least one market")
            self.assertIsInstance(markets[0], CloudMarket)
        except HaasApiError as e:
            self.fail(f"Failed to get markets: {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
