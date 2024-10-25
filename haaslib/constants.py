from enum import Enum

class OrderType(Enum):
    """Order types supported by the API"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_MARKET = "STOP_MARKET"
    STOP_LIMIT = "STOP_LIMIT"

class TimeInForce(Enum):
    """Time in force options"""
    GTC = "GTC"  # Good Till Cancel
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill

class MarketType(Enum):
    """CloudMarket types"""
    SPOT = "SPOT"
    FUTURES = "FUTURES"
    MARGIN = "MARGIN"

class ChartStyle(Enum):
    """Chart styles for backtesting"""
    CANDLESTICK = "CandleStick"
    HEIKINASHI = "HeikinAshi"
    LINE = "Line"

class Interval(Enum):
    """Time intervals"""
    M1 = 1
    M5 = 5
    M15 = 15
    M30 = 30
    H1 = 60
    H2 = 120
    H4 = 240
    D1 = 1440
