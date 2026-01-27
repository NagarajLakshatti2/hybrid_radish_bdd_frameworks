# utils/logger.py
import logging
import os

LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "execution.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("radish")

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)
