import os
import json
import unittest
import logging
import time
from datetime import datetime
from pathlib import Path
import random
import traceback  # Add this import at the top
from dotenv import load_dotenv


from haaslib.executor import RequestsExecutor, Guest, Authenticated
from haaslib.exceptions import HaasApiError, AuthenticationError
from haaslib.models.market import CloudMarket, MarketListResponse  # Add MarketListResponse here
from haaslib.models.auth import AuthResponse
from haaslib.models.base import ApiResponse
from haaslib.models.market_data import (
    MarketPrice,
    MarketPriceResponse,
    MarketPriceInformation,
    MarketPriceSummary
)


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
            self.log_response(response, "Raw MarketListResponse Response")
            
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
                        f"CloudMarket {i+1}: {market.__dict__} Details"
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
            # Step 1: Initial login
            login_params = {
                "email": self.email,
                "password": self.password,
                "interfaceSecret": self.interface_secret
            }
            
            resp = self.executor.execute_request(
                method="POST",
                endpoint="User",
                response_type=AuthResponse,
                query_params=login_params
            )
            self.log_response(resp, "Initial Login Response")
            
            self.assertTrue(resp.Success)
            self.assertIsNotNone(resp.Data)
            self.logger.info("Step 1: Initial login successful")

            # Step 2: One-time code verification
            # Add debug logging to see what's happening
            self.logger.debug(f"Response Data: {resp.Data}")
            
            # Make sure we have the necessary data from the first response
            self.assertIsNotNone(resp.Data.get('OneTimeCode'), "One-time code is missing from response")
            
            otp_params = {
                "email": self.email,
                "password": self.password,
                "interfaceSecret": self.interface_secret,
                "oneTimeCode": resp.Data.get('OneTimeCode')
            }
            
            self.logger.debug(f"OTP Parameters: {otp_params}")
            
            resp = self.executor.execute_request(
                method="POST",
                endpoint="User",
                response_type=AuthResponse,
                query_params=otp_params
            )
            self.log_response(resp, "One-time Code Response")
            
            # Add debug logging for the response
            if not resp.Success:
                self.logger.error(f"Authentication failed. Error: {resp.Error}")
                
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

    def test_03_market_details(self):
        """Test getting detailed market information"""
        try:
            # First get market list to pick a market
            markets_response = self.executor.execute(
                endpoint="Price",
                response_type=MarketListResponse,
                query_params={
                    "channel": "MARKETLIST",
                    "priceSource": test_market.price_source,
                    "baseCurrency": test_market.base_currency,
                    "quoteCurrency": test_market.quote_currency
                }
            )
            
            self.log_response(response, "CloudMarket Details Response")
            self.assertTrue(response.Success)
            self.assertIsNotNone(response.Data)
            
        except Exception as e:
            tb = traceback.format_exc()
            self.logger.error(f"Failed to get market details: {str(e)}", 
                             extra={'data': f"Traceback:\n{tb}"})
            self.fail(f"CloudMarket details test failed: {str(e)}")

    def test_04_market_price(self):
        """Test getting current market price"""
        try:
            # Get market list first
            markets_response = self.executor.execute(
                endpoint="Price",
                response_type=MarketListResponse,
                query_params={"channel": "MARKETLIST"}
            )
            
            # Filter for active markets on major exchanges
            major_exchanges = ['BINANCE']
            active_markets = [m for m in markets_response.Data 
                            if m.price_source in major_exchanges 
                            and m.enabled 
                            and m.quote_currency in ['USDT', 'BUSD']]
            
            if not active_markets:
                self.fail("No suitable test markets found")
                
            test_market = random.choice(active_markets)
            
            # Format the channel string following DEEPTICKS_EXCHANGE_PRIMARY_SECONDARY_ pattern
            channel_tag = f"PRICE_{test_market.price_source}_{test_market.base_currency}_{test_market.quote_currency}_"
            self.logger.info(f"Testing price with channel: {channel_tag}")
            
            # Get price information using the formatted channel string
            response = self.executor.execute(
                endpoint="Price",
                response_type=MarketPriceResponse,
                query_params={"channel": channel_tag}
            )
            
            self.log_response(response, "CloudMarket Price Response")
            self.assertTrue(response.Success, f"API request failed: {response.Error}")
            self.assertIsNotNone(response.Data)
            self.assertIsNotNone(response.Data.last_price)
            
        except Exception as e:
            tb = traceback.format_exc()
            self.logger.error(
                f"Failed to get market price: {str(e)}", 
                extra={'data': f"Traceback:\n{tb}"}
            )
            self.fail(f"CloudMarket price test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()
