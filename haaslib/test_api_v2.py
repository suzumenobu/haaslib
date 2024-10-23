import os
import unittest
import logging
from dotenv import load_dotenv
from typing import Optional

# Import everything we need from haaslib
from haaslib import (
    RequestsExecutor,
    Guest,
    Authenticated,
    HaasApiError,
    CloudMarket,
    ApiResponse,
    MarketList,
    get_all_markets,
    get_all_markets_by_pricesource,
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TestRequestsExecutor(unittest.TestCase):
    """Test cases for RequestsExecutor"""

    def setUp(self):
        """Set up test cases"""
        logger.info("Using API host: 127.0.0.1:8090")
        self.executor = RequestsExecutor(
            host="127.0.0.1",
            port=8090,
            state=Guest(),
            protocol="http",
            max_retries=3
        )

    def test_ping(self):
        """Test basic API connectivity"""
        response = self.executor.execute(
            endpoint="Price",
            response_type=dict,
            query_params={"channel": "PING"}
        )
        self.assertIsInstance(response, ApiResponse)
        self.assertTrue(response.Success)

    def test_authentication(self):
        """Test successful authentication"""
        try:
            authenticated_executor = self.executor.authenticate(
                email="garrypotterr@gmail.com",
                password="IQYTCQJIQYTCQJ"
            )
            self.assertIsInstance(authenticated_executor, RequestsExecutor)
            self.assertIsInstance(authenticated_executor.state, Authenticated)
        except HaasApiError as e:
            self.fail(f"Authentication failed: {e}")

    def test_authentication_failure(self):
        """Test authentication failure"""
        with self.assertRaises(HaasApiError) as context:
            self.executor.authenticate(
                email="wrong@email.com",
                password="wrongpassword"
            )
        self.assertIn("Authentication failed", str(context.exception))

    def test_get_markets(self):
        """Test getting markets list"""
        try:
            markets = get_all_markets(self.executor)
            logger.info(f"Received markets response: {markets}")
            
            self.assertIsInstance(markets, MarketList)
            self.assertIsInstance(markets.root, list)
            
            # Don't assert on non-empty list, as it might be legitimately empty
            if markets.root:
                self.assertIsInstance(markets.root[0], CloudMarket)
                logger.info(f"First market: {markets.root[0]}")
            else:
                logger.warning("Received empty market list")
        except Exception as e:
            logger.error(f"Error in test_get_markets: {str(e)}", exc_info=True)
            self.fail(f"Test failed with error: {str(e)}")

    def test_get_markets_by_pricesource(self):
        """Test getting markets filtered by price source"""
        try:
            markets = get_all_markets_by_pricesource(self.executor, "binance")
            logger.info(f"Received markets for binance: {markets}")
            
            self.assertIsInstance(markets, list)
            if markets:
                self.assertIsInstance(markets[0], CloudMarket)
                self.assertEqual(markets[0].price_source.lower(), "binance")
                logger.info(f"First binance market: {markets[0]}")
            else:
                logger.warning("No markets found for binance")
        except Exception as e:
            logger.error(f"Error in test_get_markets_by_pricesource: {str(e)}", exc_info=True)
            self.fail(f"Test failed with error: {str(e)}")

if __name__ == '__main__':
    unittest.main()
