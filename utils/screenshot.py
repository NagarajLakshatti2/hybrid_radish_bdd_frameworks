import os
import base64
from datetime import datetime

def _safe_name(name):
    return "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)

def take_screenshot(driver, name="screenshot"):
    if driver is None:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports/screenshots", exist_ok=True)

    safe_name = _safe_name(name)
    file_path = f"reports/screenshots/{safe_name}_{timestamp}.png"

    try:
        driver.save_screenshot(file_path)
        return file_path
    except Exception:
        return None

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


