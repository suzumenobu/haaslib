import os
from typing import Dict, Any

class Config:
    def __init__(self):
        self.config: Dict[str, Any] = {
            'API_HOST': os.getenv('HAAS_API_HOST', 'localhost'),
            'API_PORT': int(os.getenv('HAAS_API_PORT', '8090')),
            'API_PROTOCOL': os.getenv('HAAS_API_PROTOCOL', 'http'),
            'API_TIMEOUT': int(os.getenv('HAAS_API_TIMEOUT', '30')),
            'API_RATE_LIMIT': int(os.getenv('HAAS_API_RATE_LIMIT', '5')),
            'API_RATE_LIMIT_PERIOD': float(os.getenv('HAAS_API_RATE_LIMIT_PERIOD', '1.0')),
        }

    def get(self, key: str) -> Any:
        return self.config.get(key)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value

config = Config()