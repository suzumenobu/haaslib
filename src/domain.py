import enum
from dataclasses import dataclass
from typing import Union


class BacktestPeriodType(enum.Enum):
    MONTH = enum.auto()
    DAY = enum.auto()


@dataclass
class BacktestPeriod:
    """
    Custom wrapper for backtest periods in UNIX time.
    """

    period_type: BacktestPeriodType
    count: int

    def as_secs(self) -> int:
        """
        Get the backtest period duration in seconds.

        Returns:
            int: Backtest period duration in seconds.
        """
        match self.period_type:
            case BacktestPeriodType.MONTH:
                return 86400 * self.count
            case BacktestPeriodType.DAY:
                return int(86400 * (self.count * 30.5))

    def as_days(self) -> int:
        """
        Get the backtest period duration in days.

        Returns:
            int: Backtest period duration in days.
        """
        match self.period_type:
            case BacktestPeriodType.MONTH:
                return self.count
            case BacktestPeriodType.DAY:
                return int(self.count * 30.5)


@dataclass
class MarketTag:
    """
    Wrapper for market tags.
    """

    tag: str
