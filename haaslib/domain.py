from __future__ import annotations

import dataclasses
import enum
from datetime import datetime, timedelta


@dataclasses.dataclass
class BacktestPeriod:
    """
    Custom wrapper for backtest periods in UNIX time.
    """

    class Type(enum.Enum):
        MONTH = enum.auto()
        DAY = enum.auto()

    period_type: BacktestPeriod.Type
    count: int
    from_time: datetime = dataclasses.field(default_factory=datetime.now)

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


class HaaslibExcpetion(Exception):
    pass


@dataclasses.dataclass
class Script:
    id: str
    type: int
