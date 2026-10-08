import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BACKEND_DIR / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL environment variable is not set")


NGINX_PROXY_TOKEN = os.getenv("NGINX_PROXY_TOKEN")

if not NGINX_PROXY_TOKEN:
    raise RuntimeError("NGINX_PROXY_TOKEN environment variable is not set")