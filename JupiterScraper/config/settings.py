"""
Global settings and configuration for Jupiter.money RAG Bot
"""

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / "cache"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Website configuration
BASE_URL = "https://www.jupiter.money"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Data configuration
DATA_FILE = DATA_DIR / "scraped_texts.txt"
CACHE_FILE = CACHE_DIR / "cache_metadata.json"
CHUNK_SIZE = 500
TOP_K = 5

# Timing configuration
REFRESH_INTERVAL = 6 * 60 * 60  # 6 hours in seconds
REQUEST_DELAY = 2  # seconds between requests
PAGE_TIMEOUT = 15  # seconds timeout for page loading

# Scraping configuration
MAX_PAGES = 100
MAX_RETRIES = 3
HEADLESS_MODE = True

# NLP configuration
MIN_SIMILARITY_THRESHOLD = 0.15
MAX_VOCABULARY_SIZE = 10000
SYNONYM_EXPANSION = True

# UI configuration
PAGE_TITLE = "Jupiter Assistant"
PAGE_ICON = "🟢"
LAYOUT = "wide"

# Environment variables (with defaults)
DEBUG_MODE = os.getenv("JUPITER_SCRAPER_DEBUG", "false").lower() == "true"
MAX_PAGES_ENV = int(os.getenv("JUPITER_SCRAPER_MAX_PAGES", str(MAX_PAGES)))
TIMEOUT_ENV = int(os.getenv("JUPITER_SCRAPER_TIMEOUT", str(PAGE_TIMEOUT)))

# Override with environment variables if set
MAX_PAGES = MAX_PAGES_ENV
PAGE_TIMEOUT = TIMEOUT_ENV 