# utils/browser.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.config import HEADLESS


def get_web_driver():
    options = Options()
    options.add_argument("--start-maximized")

    if HEADLESS:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 🔎 HARD ASSERT — this will END the confusion
    assert hasattr(driver, "get"), f"Not a Selenium driver: {type(driver)}"

    return driver
