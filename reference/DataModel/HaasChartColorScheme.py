import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasChartColorScheme:
    Font: Any
    Axis: Any
    Grid: Any
    Text: Any
    Background: Any
    PriceGhostLine: Any
    VolumeGhostLine: Any
