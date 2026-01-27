import allure
from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import WEB_BASE_URL, WEB_USERNAME, WEB_PASSWORD


@given(r"I open the login page")
def open_login_page(step):
    step.context.driver.get(WEB_BASE_URL)
    step.context.logger.info("User login successfully")


@when(r"I login with valid credentials")
def login(step):
    driver = step.context.driver
    wait = WebDriverWait(driver, 10)

    username = wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    password = driver.find_element(By.ID, "password")
    sign_in = driver.find_element(By.ID, "signInBtn")

    username.clear()
    username.send_keys(WEB_USERNAME)

    password.clear()
    password.send_keys(WEB_PASSWORD)

    sign_in.click()
    step.context.logger.info("User login successfully")


@then("I should be logged in")
def verify_login(step):
    driver = step.context.driver
    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".nav-link"))
    )
    step.context.logger.info("User logged in successfully")

