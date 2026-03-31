# Web application config
import os

# ---------- ENV ----------
ENV = os.getenv("ENV", "qa")

# ---------- HEADLESS & BROWSER ----------
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BROWSER = os.getenv("BROWSER", "chrome")

# ---------- WEB ----------
WEB_BASE_URL = os.getenv(
    "WEB_BASE_URL",
    "https://rahulshettyacademy.com/loginpagePractise/"
)

WEB_USERNAME = os.getenv("WEB_USERNAME", "rahulshettyacademy")
WEB_PASSWORD = os.getenv("WEB_PASSWORD", "Learning@830$3mK2")

WEB_INVALID_USERNAME = os.getenv("WEB_INVALID_USERNAME", "rahulshetty")
WEB_INVALID_PASSWORD = os.getenv("WEB_INVALID_PASSWORD", "Learning@830$")

