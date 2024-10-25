from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8090
    API_PROTOCOL: str = "http"
    API_EMAIL: Optional[str] = None
    API_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings()
