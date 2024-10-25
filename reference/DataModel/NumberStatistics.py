import dataclasses
from typing import List

@dataclasses.dataclass
class NumberStatistics:
    Min: float
    Max: float
    Avg: float
    Median: float
    Values: List[float]
