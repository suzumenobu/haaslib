import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    API_HOST = os.getenv('HAAS_API_HOST', '127.0.0.1')
    API_PORT = int(os.getenv('HAAS_API_PORT', '8090'))
    API_EMAIL = os.getenv('HAAS_API_EMAIL')
    API_PASSWORD = os.getenv('HAAS_API_PASSWORD')

config = Config()
