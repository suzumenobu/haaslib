import unittest
# Update import to use consolidated version
from ..models.market import CloudMarket, MarketList
from ..domain import MarketTag

class TestModels(unittest.TestCase):
    def test_cloud_market(self):
        """Test CloudMarket model"""
        market_data = {
            "Id": "BINANCE_BTC_USDT",
            "Name": "BTC/USDT",
            "PriceSource": "BINANCE",
            "BaseCurrency": "BTC",
            "QuoteCurrency": "USDT",
            "Enabled": True
        }
        market = CloudMarket(**market_data)
        self.assertEqual(market.id, "BINANCE_BTC_USDT")
        self.assertEqual(market.as_market_tag(), "BINANCE_BTC_USDT_SPOT")

    def test_market_list(self):
        """Test MarketList model"""
        markets_data = {
            "root": [
                {
                    "id": "BINANCE_BTC_USDT",
                    "name": "BTC/USDT",
                    "price_source": "BINANCE",
                    "base_currency": "BTC",
                    "quote_currency": "USDT",
                    "enabled": True
                }
            ]
        }
        market_list = MarketList(**markets_data)
        self.assertEqual(len(market_list.root), 1)
        self.assertIsInstance(market_list.root[0], CloudMarket)

    def test_create_lab_request(self):
        """Test CreateLabRequest model"""
        request_data = {
            "script_id": "test_script",
            "name": "Test Lab",
            "account_id": "test_account",
            "market": "BINANCE_BTC_USDT_SPOT",
            "interval": 15,
            "default_price_data_style": "CandleStick"
        }
        request = CreateLabRequest(**request_data)
        self.assertEqual(request.script_id, "test_script")
        self.assertEqual(request.interval, 15)
