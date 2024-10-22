import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_HOST: str = os.getenv('HAAS_API_HOST', '127.0.0.1')
    API_PORT: int = int(os.getenv('HAAS_API_PORT', '8090'))
    API_EMAIL: str = os.getenv('HAAS_API_EMAIL', '')
    API_PASSWORD: str = os.getenv('HAAS_API_PASSWORD', '')
    BASE_URL: str = f"http://{API_HOST}:{API_PORT}"  # Changed to HTTP

config = Config()
