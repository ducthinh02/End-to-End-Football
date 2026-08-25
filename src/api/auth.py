import os 
from dotenv import load_dotenv
from src.core.Exceptions import ConfigurationError

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
TIMEOUT = int(os.getenv("TIME_OUT","30"))

if not API_KEY:
    raise ConfigurationError("API_KEY not found in .env")

if not API_BASE_URL:
    raise ConfigurationError("API_BASE_URL not found in .env")

HEADERS = {
    "X-Auth-Token" : API_KEY
}