import os
import allure
from allure_commons.types import AttachmentType


def attach_screenshot(driver, name="Failure Screenshot"):
    if not driver:
        return
    png = driver.get_screenshot_as_png()
    allure.attach(
        png,
        name=name,
        attachment_type=AttachmentType.PNG
    )

def attach_debug_info(driver):
    allure.attach(
        driver.current_url,
        name="Current URL",
        attachment_type=AttachmentType.TEXT
    )
    allure.attach(
        driver.title,
        name="Page Title",
        attachment_type=AttachmentType.TEXT
    )

import os
from datetime import datetime

def save_screenshot(driver, scenario_name):
    os.makedirs("reports/screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{scenario_name}_{timestamp}.png".replace(" ", "_")
    path = os.path.join("reports/screenshots", filename)
    driver.save_screenshot(path)

