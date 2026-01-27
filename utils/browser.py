import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_web_driver():
    options = Options()

    # Headless for CI
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # REQUIRED for GitHub Actions / Docker / Jenkins
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Stability
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-allow-origins=*")

    service = Service()  # GitHub runner already has chromedriver

    driver = webdriver.Chrome(service=service, options=options)
    return driver
