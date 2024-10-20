import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from dotenv import load_dotenv

from haaslib.api import RequestsExecutor, get_all_markets, get_accounts, HaasApiError, Guest, Authenticated
from haaslib.model import CloudMarket, UserAccount

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
        print(f"Attempting authentication for {self.email}...")
        authenticated_executor = self.executor.authenticate(email=self.email, password=self.password)
        self.assertIsInstance(authenticated_executor, RequestsExecutor)
        self.assertIsInstance(authenticated_executor.state, Authenticated)
        print("Authentication successful.")

    def test_get_markets(self):
        authenticated_executor = self.get_authenticated_executor()
        markets = get_all_markets(authenticated_executor)
        self.assertIsInstance(markets, list)
        self.assertTrue(len(markets) > 0)
        for market in markets:
            self.assertIsInstance(market, CloudMarket)

    def test_get_accounts(self):
        authenticated_executor = self.executor.authenticate(email=self.email, password=self.password)
        accounts = get_accounts(authenticated_executor)
        self.assertIsInstance(accounts, list)
        if len(accounts) > 0:
            self.assertIsInstance(accounts[0], UserAccount)
        print(f"Retrieved {len(accounts)} accounts.")

    def get_authenticated_executor(self):
        return self.executor.authenticate(email=self.email, password=self.password)

if __name__ == '__main__':
    unittest.main(verbosity=2)
