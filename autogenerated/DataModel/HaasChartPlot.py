import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasChartPlot:
    PlotId: str
    PlotIndex: int
    Title: str
    Height: int
    IsSignalPlot: bool
    RightAxis: bool
    LeftAxis: bool
    PricePlot: Any
    DataLines: List[Any]
    Shapes: List[Any]
    Annotations: List[Any]
    TradeAnnotations: List[Any]
