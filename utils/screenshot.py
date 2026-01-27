import os
from datetime import datetime

SCREENSHOT_DIR = "reports/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(driver, name):
    safe_name = name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{SCREENSHOT_DIR}/{safe_name}_{timestamp}.png"
    driver.save_screenshot(file_path)
    return file_path
