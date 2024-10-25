import dataclasses

@dataclasses.dataclass
class UserLabConfig:
    MaxPopulation: int
    MaxGenerations: int
    MaxElites: int
    MixRate: float
    AdjustRate: float
