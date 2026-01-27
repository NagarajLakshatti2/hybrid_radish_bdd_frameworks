from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.step_markers import mark_step_screenshot, mark_step_log
from utils.screenshot import take_screenshot

from utils.config import (
    WEB_BASE_URL,
    WEB_USERNAME,
    WEB_PASSWORD,
    WEB_INVALID_USERNAME,
    WEB_INVALID_PASSWORD,
)

@given("I open the login page")
def open_login_page(step):
    driver = step.context.driver
    driver.get(WEB_BASE_URL)

    shot = take_screenshot(driver, "OPEN_LOGIN")
    mark_step_screenshot(step, shot)
    mark_step_log(step, step.context.log_path)

    step.context.logger.info("Opened login page")


@when("I login with valid credentials")
def login_valid(step):
    driver = step.context.driver
    wait = WebDriverWait(driver, 10)

    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password = driver.find_element(By.ID, "password")
    sign_in = driver.find_element(By.ID, "signInBtn")

    username.clear()
    username.send_keys(WEB_USERNAME)

    password.clear()
    password.send_keys(WEB_PASSWORD)

    sign_in.click()

    shot = take_screenshot(driver, "LOGIN_VALID")
    mark_step_screenshot(step, shot)
    mark_step_log(step, step.context.log_path)

    step.context.logger.info("Login with valid credentials submitted")


@then("I should be logged in")
def verify_login(step):
    driver = step.context.driver
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".nav-link")))

    shot = take_screenshot(driver, "LOGIN_SUCCESS")
    mark_step_screenshot(step, shot)
    mark_step_log(step, step.context.log_path)

    step.context.logger.info("User logged in successfully")


@when("I login with invalid credentials")
def login_invalid(step):
    driver = step.context.driver
    wait = WebDriverWait(driver, 10)

    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password = driver.find_element(By.ID, "password")
    sign_in = driver.find_element(By.ID, "signInBtn")

    username.clear()
    username.send_keys(WEB_INVALID_USERNAME)

    password.clear()
    password.send_keys(WEB_INVALID_PASSWORD)

    sign_in.click()

    shot = take_screenshot(driver, "LOGIN_INVALID")
    mark_step_screenshot(step, shot)
    mark_step_log(step, step.context.log_path)

    step.context.logger.error("Login failed with invalid credentials")

    raise AssertionError("Invalid login scenario failed as expected")
