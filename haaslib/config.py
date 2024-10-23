import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load the .env file
load_dotenv()

class Config(BaseModel):
    API_HOST: str = os.getenv('HAAS_API_HOST', '127.0.0.1')
    API_PORT: int = int(os.getenv('HAAS_API_PORT', '8090'))
    API_PROTOCOL: str = os.getenv('HAAS_API_PROTOCOL', 'http')
    API_EMAIL: str = os.getenv('HAAS_API_EMAIL', '')
    API_PASSWORD: str = os.getenv('HAAS_API_PASSWORD', '')
    LOG_LEVEL: str = os.getenv('HAAS_LOG_LEVEL', 'INFO')

    class Config:
        env_prefix = 'HAAS_'
        case_sensitive = False

config = Config()
