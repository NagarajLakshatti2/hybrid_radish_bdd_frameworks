from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import WEB_BASE_URL, WEB_USERNAME, WEB_PASSWORD


class LoginPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- LOCATORS ----------
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SIGNIN = (By.ID, "signInBtn")

    # A reliable post-login element on this site
    SUCCESS_TEXT = (By.CSS_SELECTOR, ".nav-link.btn.btn-primary")

    # ---------- ACTIONS ----------
    def open(self):
        self.driver.get(WEB_BASE_URL)

    def login_valid_user(self):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)) \
            .send_keys(WEB_USERNAME)

        self.driver.find_element(*self.PASSWORD) \
            .send_keys(WEB_PASSWORD)

        self.driver.find_element(*self.SIGNIN).click()

    def verify_login_success(self):
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TEXT))
