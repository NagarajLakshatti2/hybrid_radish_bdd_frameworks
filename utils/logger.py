import logging
import os

LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(scenario_id):
    log_path = f"{LOG_DIR}/scenario_{scenario_id}.log"

    logger = logging.getLogger(f"scenario_{scenario_id}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger, log_path
