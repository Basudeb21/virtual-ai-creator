#config/platform_api.py
import os
from dotenv import load_dotenv

load_dotenv()

API_REGISTER_URL = os.getenv('API_REGISTER_URL')