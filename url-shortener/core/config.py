import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
URL_SHORT_STORAGE_FILE = BASE_DIR / "short_urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
