# Web application config
import os
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


# ---------- ENV ----------
ENV = os.getenv("ENV", "qa")

# ---------- WEB ----------
WEB_BASE_URL = os.getenv(
    "WEB_BASE_URL",
    "https://rahulshettyacademy.com/loginpagePractise/"
)

WEB_USERNAME = os.getenv("WEB_USERNAME", "rahulshettyacademy")
WEB_PASSWORD = os.getenv("WEB_PASSWORD", "Learning@830$3mK2")

# ---------- BROWSER ----------
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
