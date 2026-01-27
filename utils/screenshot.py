import os
import base64
from datetime import datetime

SCREENSHOT_DIR = "reports/screenshots"

def _safe_name(name):
    return "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)

def take_screenshot(driver, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{SCREENSHOT_DIR}/{name}_{ts}.png"
    driver.save_screenshot(path)
    return path

def attach_screenshot_to_step(step, file_path):
    if not file_path or not os.path.exists(file_path):
        return

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    step.attach(
        encoded,
        mime_type="image/png",
        description="Screenshot"
    )
