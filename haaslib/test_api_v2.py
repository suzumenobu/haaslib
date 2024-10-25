import os
import json
import unittest
import logging
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import random

from haaslib.executor import RequestsExecutor, Guest, Authenticated
from haaslib.exceptions import HaasApiError, AuthenticationError
from haaslib.models.market import CloudMarket
from haaslib.models.auth import AuthResponse
from haaslib.models.base import ApiResponse
from haaslib.models.market import MarketListResponse


class TestRequestsExecutor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load environment variables before tests"""
        load_dotenv()
        
        # Configure logging
        cls.logger = logging.getLogger('haaslib.test')
        cls.logger.setLevel(logging.DEBUG)
        
        # Add console handler if not already present
        if not cls.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            cls.logger.addHandler(console_handler)
        
        # Verify required environment variables
        required_vars = ['HAAS_API_HOST', 'HAAS_API_EMAIL', 'HAAS_API_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.logger.info("Setting up test executor...")
        
        # Create guest executor
        self.guest_executor = RequestsExecutor[Guest](
            base_url=os.getenv('HAAS_API_HOST'),
            email=os.getenv('HAAS_API_EMAIL'),
            password=os.getenv('HAAS_API_PASSWORD'),
            port=os.getenv('HAAS_API_PORT')
        )
        
        try:
            # Authenticate and get authenticated executor
            self.logger.info("Attempting authentication...")
            self.executor = self.guest_executor.authenticate()
            self.assertIsInstance(self.executor.state, Authenticated)
            self.assertIsNotNone(
                self.executor.state.interface_secret,
                "No interface key available after authentication"
            )
            self.logger.info("Successfully authenticated")
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            self.fail(f"Authentication failed: {str(e)}")
        
        self.test_delay = 1  # Delay between tests in seconds

    def tearDown(self):
        """Clean up after each test"""
        time.sleep(self.test_delay)  # Rate limiting

    def test_01_market_list(self):
        """Test getting markets list"""
        try:
            self.logger.info("Testing market list retrieval...")
            response = self.executor.execute(
                endpoint="Price",
                response_type=MarketListResponse,  # Changed from list[CloudMarket]
                query_params={"channel": "MARKETLIST"}
            )
            self.assertTrue(response.Success)
            self.assertIsNotNone(response.Data)
            
            markets = response.Data  # Now we get the list from response.Data
            self.assertIsInstance(markets, list)
            self.logger.info(f"Found {len(markets)} markets")
            
            if markets:
                self.logger.debug(f"First market: {markets[0].dict()}")
                
        except Exception as e:
            self.logger.error(f"Failed to get markets: {str(e)}")
            self.fail(f"Failed to get markets: {str(e)}")

    def test_02_authentication_flow(self):
        """Test the two-step authentication process"""
        try:
            self.logger.info("Testing authentication flow...")
            
            # Step 1: Initial login
            interface_secret = "".join(str(random.randint(0, 100)) for _ in range(10))
            self.logger.debug(f"Generated interface key: {interface_secret}")
            
            resp = self.guest_executor.execute(
                endpoint="User",
                response_type=AuthResponse,
                query_params={
                    "channel": "LOGIN_WITH_CREDENTIALS",
                    "email": os.getenv('HAAS_API_EMAIL'),
                    "password": os.getenv('HAAS_API_PASSWORD'),
                    "interfaceKey": interface_secret
                }
            )
            self.assertTrue(resp.Success)
            self.logger.info("Step 1: Initial login successful")
            
            # Step 2: One-time code
            resp = self.guest_executor.execute(
                endpoint="User",
                response_type=AuthResponse,
                query_params={
                    "channel": "LOGIN_WITH_ONE_TIME_CODE",
                    "email": os.getenv('HAAS_API_EMAIL'),
                    "pincode": random.randint(100_000, 200_000),
                    "interfaceKey": interface_secret
                }
            )
            self.assertTrue(resp.Success)
            self.assertIsNotNone(resp.Data)
            self.logger.info("Step 2: One-time code authentication successful")
            
        except Exception as e:
            self.logger.error(f"Authentication flow test failed: {str(e)}")
            self.fail(f"Authentication flow test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()
