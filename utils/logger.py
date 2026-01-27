import logging
import os

LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_scenario_logger(scenario_id):
    log_file = os.path.join(LOG_DIR, f"scenario_{scenario_id}.log")

    logger = logging.getLogger(f"radish-{scenario_id}")
    logger.setLevel(logging.INFO)

    # 🔴 avoid duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(message)s"
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger, log_file
