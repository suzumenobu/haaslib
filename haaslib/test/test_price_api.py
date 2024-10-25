import unittest
import logging
from typing import List
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Add this at the top of the file
def setup_logging():
    """Setup logging to both file and console"""
    # Create logs directory if it doesn't exist
    log_file = "logs.txt"
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Get the root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

from ..executor import RequestsExecutor, Guest, Authenticated
from ..api.price import (
    get_server_time,
    get_all_pricesources_simple,
    get_pricesources_detailed,
    get_all_markets,
    get_all_markets_by_source,
    get_unique_markets,
    get_markets_by_source,
    get_trade_markets,
    get_coin_list,
    get_price,
    get_orderbook,
    get_last_trades,
    get_sync_ticks,
    get_last_ticks,
    get_deep_ticks,
    get_price_snapshot,
    get_custom_snapshot_minute_tick
)

class TestPriceAPI(unittest.TestCase):
    """Test cases for Price API endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up test executor with authentication"""
        # Setup logging first
        cls.logger = setup_logging()
        cls.logger.info("Starting Price API tests")
        
        # Load environment variables
        load_dotenv()
        
        # Create executor and authenticate
        cls.executor = RequestsExecutor(
            base_url="127.0.0.1",  # Changed from full URL to just host
            port="8090",
            email=os.getenv('HAAS_API_EMAIL'),
            password=os.getenv('HAAS_API_PASSWORD'),
            state=Guest()
        )
        
        # Authenticate
        cls.executor = cls.executor.authenticate()
        
        cls.logger.info("Test executor initialized and authenticated")

    def test_01_server_time(self):
        """Test getting server time"""
        try:
            time = get_server_time(self.executor)
            self.assertIsInstance(time, int)
            self.logger.info(f"Server time: {datetime.fromtimestamp(time)}")
        except Exception as e:
            self.fail(f"Failed to get server time: {str(e)}")

    def test_02_price_sources(self):
        """Test getting price sources"""
        try:
            # Test simple list
            sources = get_all_pricesources_simple(self.executor)
            self.assertIsInstance(sources, list)
            self.assertTrue(len(sources) > 0)
            self.logger.info(f"Found {len(sources)} price sources")
            
            # Test detailed list
            detailed = get_pricesources_detailed(self.executor)
            self.assertIsInstance(detailed, list)
            self.assertTrue(len(detailed) > 0)
            
            # Log some details about the first source
            if detailed:
                first = detailed[0]
                self.logger.info(
                    f"Example source: {first.full_name} ({first.friendly_name})"
                    f" - Enabled: {first.enabled}"
                )
            
        except Exception as e:
            self.fail(f"Failed to get price sources: {str(e)}")

    def test_03_markets(self):
        """Test getting markets"""
        try:
            # Test all markets
            markets = get_all_markets(self.executor)
            self.assertIsInstance(markets, list)
            self.assertTrue(len(markets) > 0)
            self.logger.info(f"Found {len(markets)} total markets")
            
            # Test markets by source
            markets_by_source = get_all_markets_by_source(self.executor)
            self.assertIsInstance(markets_by_source, dict)
            self.assertTrue(len(markets_by_source) > 0)
            
            # Test unique markets
            unique = get_unique_markets(self.executor)
            self.assertIsInstance(unique, list)
            self.assertTrue(len(unique) > 0)
            
            # Test specific source markets (using BINANCE as example)
            binance_markets = get_markets_by_source(self.executor, "BINANCE")
            self.assertIsInstance(binance_markets, list)
            self.assertTrue(len(binance_markets) > 0)
            
            # Test trade markets
            trade_markets = get_trade_markets(self.executor, "BINANCE")
            self.assertIsInstance(trade_markets, list)
            self.logger.info(f"Found {len(trade_markets)} BINANCE trade markets")
            
        except Exception as e:
            self.fail(f"Failed to get markets: {str(e)}")

    def test_04_coin_list(self):
        """Test getting coin list"""
        try:
            coins = get_coin_list(self.executor)
            self.assertIsInstance(coins, list)
            self.assertTrue(len(coins) > 0)
            self.logger.info(f"Found {len(coins)} coins")
        except Exception as e:
            self.fail(f"Failed to get coin list: {str(e)}")

    def test_05_market_data(self):
        """Test getting market data"""
        try:
            # Get a test market from BINANCE
            markets = get_markets_by_source(self.executor, "BINANCE")
            test_market = next(
                (m for m in markets 
                 if m.base_currency == "BTC" and m.quote_currency == "USDT"),
                None
            )
            if not test_market:
                self.fail("Could not find BTC/USDT market for testing")
                
            market_tag = f"{test_market.price_source}_{test_market.base_currency}_{test_market.quote_currency}_"
            
            # Test price
            price_data = get_price(self.executor, market_tag)
            self.assertIsInstance(price_data, MarketPrice)
            self.assertTrue(price_data.close > 0)
            self.logger.info(
                f"BTC price: {price_data.close} "
                f"(Bid: {price_data.bid}, Ask: {price_data.ask})"
            )
            
            # Test orderbook
            book = get_orderbook(self.executor, market_tag)
            self.assertIsNotNone(book)
            self.assertTrue(len(book.bids) > 0)
            self.assertTrue(len(book.asks) > 0)
            
            # Test last trades
            trades = get_last_trades(self.executor, market_tag)
            self.assertIsInstance(trades, list)
            self.assertTrue(len(trades) > 0)
            
            # Test sync ticks
            ticks = get_sync_ticks(self.executor, market_tag)
            self.assertIsInstance(ticks, list)
            self.assertTrue(len(ticks) > 0)
            
            # Test last ticks
            last_ticks = get_last_ticks(self.executor, market_tag, interval=15)
            self.assertIsInstance(last_ticks, list)
            self.assertTrue(len(last_ticks) > 0)
            
            # Test deep ticks
            deep_ticks = get_deep_ticks(self.executor, market_tag)
            self.assertIsInstance(deep_ticks, list)
            self.assertTrue(len(deep_ticks) > 0)
            
        except Exception as e:
            self.fail(f"Failed to get market data: {str(e)}")

    def test_06_snapshot(self):
        """Test getting price snapshot"""
        try:
            snapshot = get_price_snapshot(self.executor, "BINANCE")
            self.assertIsInstance(snapshot, list)
            self.assertTrue(len(snapshot) > 0)
        except Exception as e:
            self.fail(f"Failed to get price snapshot: {str(e)}")

    def test_07_custom_snapshot(self):
        """Test getting custom snapshot minute tick"""
        try:
            # Get some test markets
            markets = [
                "BINANCEQUARTERLY_SOL_USD_QUARTERLY",
                "BINANCEQUARTERLY_ETH_USD_QUARTERLY"
            ]
            
            snapshot = get_custom_snapshot_minute_tick(self.executor, markets)
            self.assertIsInstance(snapshot, list)
            self.logger.info(f"Got custom snapshot for {len(markets)} markets")
            
        except Exception as e:
            self.fail(f"Failed to get custom snapshot: {str(e)}")

if __name__ == '__main__':
    unittest.main()
