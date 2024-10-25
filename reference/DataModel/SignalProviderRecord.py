import dataclasses

@dataclasses.dataclass
class SignalProviderRecord:
    Id: str
    UserId: str
    Name: str
    Description: str
    SecretKey: str
    Published: int
