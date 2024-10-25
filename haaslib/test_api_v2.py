import os
import json
import unittest
import logging
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import random
import traceback  # Add this import at the top

from haaslib.executor import RequestsExecutor, Guest, Authenticated
from haaslib.exceptions import HaasApiError, AuthenticationError
from haaslib.models.market import Market
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
        
        # Add file handler
        file_handler = logging.FileHandler('logs.txt', mode='w')  # 'w' mode to overwrite
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
            'Additional Data:\n%(data)s\n',
            defaults={'data': ''}
        )
        file_handler.setFormatter(file_formatter)
        cls.logger.addHandler(file_handler)
        
        # Add console handler if not already present
        if not any(isinstance(h, logging.StreamHandler) for h in cls.logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)  # Less verbose for console
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
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

    def log_response(self, response, message="API Response"):
        """Helper to log response with pretty-printed JSON"""
        try:
            if hasattr(response, 'dict'):
                response_data = response.dict()
            else:
                response_data = response
            formatted_json = json.dumps(response_data, indent=2)
            self.logger.debug(
                message,
                extra={'data': f"Response Data:\n{formatted_json}"}
            )
        except Exception as e:
            self.logger.error(f"Failed to log response: {str(e)}")

    def test_01_market_list(self):
        """Test getting markets list"""
        try:
            self.logger.info("Testing market list retrieval...")
            
            # Log request details
            self.logger.debug(
                "Making market list request",
                extra={'data': json.dumps({
                    'endpoint': "Price",
                    'response_type': "MarketListResponse",
                    'query_params': {"channel": "MARKETLIST"}
                }, indent=2)}
            )
            
            response = self.executor.execute(
                endpoint="Price",
                response_type=MarketListResponse,
                query_params={"channel": "MARKETLIST"}
            )
            
            # Log raw response
            self.log_response(response, "Raw MarketList Response")
            
            self.assertTrue(response.Success)
            self.assertIsNotNone(response.Data)
            
            markets = response.Data
            self.assertIsInstance(markets, list)
            self.logger.info(f"Found {len(markets)} markets")
            
            if markets:
                # Log first few markets in detail
                for i, market in enumerate(markets[:3]):
                    self.log_response(
                        market.__dict__,
                        f"Market {i+1}: {market.__dict__} Details"
                    )
                
        except Exception as e:
            # Get the full traceback
            tb = traceback.format_exc()
            self.logger.error(
                f"Failed to get markets: {str(e)}",
                extra={'data': f"Exception details:\n{str(e)}\n\nTraceback:\n{tb}"}
            )
            self.fail(f"Failed to get markets: {str(e)}")

    def test_02_authentication_flow(self):
        """Test the two-step authentication process"""
        try:
            self.logger.info("Testing authentication flow...")
            
            # Step 1: Initial login
            interface_secret = "".join(str(random.randint(0, 100)) for _ in range(10))
            
            login_params = {
                "channel": "LOGIN_WITH_CREDENTIALS",
                "email": os.getenv('HAAS_API_EMAIL'),
                "password": "***REDACTED***",  # Don't log actual password
                "interfaceKey": interface_secret
            }
            self.logger.debug(
                "Making initial login request",
                extra={'data': json.dumps(login_params, indent=2)}
            )
            
            resp = self.guest_executor.execute(
                endpoint="User",
                response_type=AuthResponse,
                query_params=login_params
            )
            self.log_response(resp, "Initial Login Response")
            
            self.assertTrue(resp.Success)
            self.logger.info("Step 1: Initial login successful")
            
            # Step 2: One-time code
            pincode = random.randint(100_000, 200_000)
            otp_params = {
                "channel": "LOGIN_WITH_ONE_TIME_CODE",
                "email": os.getenv('HAAS_API_EMAIL'),
                "pincode": pincode,
                "interfaceKey": interface_secret
            }
            self.logger.debug(
                "Making one-time code request",
                extra={'data': json.dumps(otp_params, indent=2)}
            )
            
            resp = self.guest_executor.execute(
                endpoint="User",
                response_type=AuthResponse,
                query_params=otp_params
            )
            self.log_response(resp, "One-time Code Response")
            
            self.assertTrue(resp.Success)
            self.assertIsNotNone(resp.Data)
            self.logger.info("Step 2: One-time code authentication successful")
            
        except Exception as e:
            tb = traceback.format_exc()
            self.logger.error(
                f"Authentication flow test failed: {str(e)}",
                extra={'data': f"Exception details:\n{str(e)}\n\nTraceback:\n{tb}"}
            )
            self.fail(f"Authentication flow test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()
