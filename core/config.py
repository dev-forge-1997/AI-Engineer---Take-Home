import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "demo").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "1"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
GEMINI_MIN_REQUEST_INTERVAL = float(os.getenv("GEMINI_MIN_REQUEST_INTERVAL", "5"))
