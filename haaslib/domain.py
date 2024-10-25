from __future__ import annotations

import dataclasses
import enum
from datetime import datetime, timedelta
from typing import Literal, Optional


@dataclasses.dataclass
class BacktestPeriod:
    """
    Custom wrapper for backtest periods in UNIX time.
    """

    class Type(enum.Enum):
        MINUTE = enum.auto()
        HOUR = enum.auto()
        DAY = enum.auto()
        WEEK = enum.auto()
        MONTH = enum.auto()
        YEAR = enum.auto()

    period_type: BacktestPeriod.Type
    count: int
    custom_start: Optional[int] = None
    custom_end: Optional[int] = None

    def as_secs(self) -> int:
        """
        Get the backtest period duration in seconds.

        Returns:
            int: Backtest period duration in seconds.
        """
        match self.period_type:
            case BacktestPeriod.Type.MONTH:
                return 86400 * self.count
            case BacktestPeriod.Type.DAY:
                return int(86400 * (self.count * 30.5))

        raise ValueError(f"Unknown period type: {self.period_type}")

    def as_days(self) -> int:
        """
        Get the backtest period duration in days.

        Returns:
            int: Backtest period duration in days.
        """
        match self.period_type:
            case BacktestPeriod.Type.MONTH:
                return self.count
            case BacktestPeriod.Type.DAY:
                return int(self.count * 30.5)

        raise ValueError(f"Unknown period type: {self.period_type}")

    @property
    def start_unix(self) -> int:
        return int(self.from_time.timestamp())

    @property
    def end_unix(self) -> int:
        return int((self.from_time - timedelta(seconds=self.as_secs())).timestamp())


@dataclasses.dataclass
class MarketTag:
    """
    Wrapper for market tags.
    """

    tag: str

    @classmethod
    def from_components(
        cls,
        price_source: str,
        base: str,
        quote: str,
        market_type: str = "SPOT"
    ) -> MarketTag:
        """Create market tag from components"""
        return cls(f"{price_source}_{base}_{quote}_{market_type}")

    def __str__(self) -> str:
        return self.tag


class HaaslibException(Exception):
    pass


@dataclasses.dataclass
class Script:
    id: str
    type: int

PriceDataStyle = Literal[
    "CandleStick",
    "CandleStickHLC",
    "HeikinAshi",
    "OHLC",
    "HLC",
    "CloseLine",
    "Line",
    "Mountain",
]


@dataclasses.dataclass
class ScriptParameter:
    """Script parameter configuration"""
    name: str
    value: str
    parameter_type: str
