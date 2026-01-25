import os
from datetime import datetime

SCREENSHOT_DIR = "reports/screenshots"


def save_screenshot(driver, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_").replace("/", "_")
    path = f"{SCREENSHOT_DIR}/{safe_name}_{timestamp}.png"

    driver.save_screenshot(path)
    return path
