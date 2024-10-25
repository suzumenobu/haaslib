import dataclasses

@dataclasses.dataclass
class HaasChartCandle:
    O: float
    H: float
    L: float
    C: float
    V: float
    M: int
