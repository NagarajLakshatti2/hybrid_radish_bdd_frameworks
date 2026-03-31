"""
Web Login Step Definitions for Radish BDD Framework

Related Feature File: features/web/login.feature

Step Navigation Guide (for PyCharm IDE):
- Press Ctrl+Shift+F to find steps from feature file
- Mark radish/steps/ as Sources Root for better IDE support
- Install Gherkin plugin: File → Settings → Plugins → Search "Gherkin" → Install

Step Coverage:
- Given "I open the login page" → open_login_page()
- When "I login with valid credentials" → login_valid()
- Then "I should be logged in" → verify_login()
- When "I login with invalid credentials" → login_invalid()
- Then "login should fail" → verify_login_failure()
"""

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

import allure  # Add Allure import

@given("I open the login page")
def open_login_page(step):
    with allure.step("Open login page"):
        driver = step.context.driver
        driver.get(WEB_BASE_URL)

        # Attach screenshot to Allure
        allure.attach(driver.get_screenshot_as_png(), name="Login Page",
                     attachment_type=allure.attachment_type.PNG)

        shot = take_screenshot(driver, "OPEN_LOGIN")
        mark_step_screenshot(step, shot)
        mark_step_log(step, step.context.log_path)

        step.context.logger.info("Opened login page")


@when("I login with valid credentials")
def login_valid(step):
    with allure.step("Login with valid credentials"):
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

        # Attach screenshot to Allure
        allure.attach(driver.get_screenshot_as_png(), name="After Login Attempt",
                     attachment_type=allure.attachment_type.PNG)

        shot = take_screenshot(driver, "LOGIN_VALID")
        mark_step_screenshot(step, shot)
        mark_step_log(step, step.context.log_path)

        step.context.logger.info("Login with valid credentials submitted")


@then("I should be logged in")
def verify_login(step):
    with allure.step("Verify successful login"):
        driver = step.context.driver
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".nav-link")))

        # Attach screenshot to Allure
        allure.attach(driver.get_screenshot_as_png(), name="Login Success",
                     attachment_type=allure.attachment_type.PNG)

        shot = take_screenshot(driver, "LOGIN_SUCCESS")
        mark_step_screenshot(step, shot)
        mark_step_log(step, step.context.log_path)

        step.context.logger.info("User logged in successfully")


@when("I login with invalid credentials")
def login_invalid(step):
    with allure.step("Login with invalid credentials"):
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

        # Attach screenshot to Allure
        allure.attach(driver.get_screenshot_as_png(), name="After Invalid Login Attempt",
                     attachment_type=allure.attachment_type.PNG)

        shot = take_screenshot(driver, "LOGIN_INVALID")
        mark_step_screenshot(step, shot)
        mark_step_log(step, step.context.log_path)

        step.context.logger.warning("Login with invalid credentials submitted")


@then("login should fail")
def verify_login_failure(step):
    with allure.step("Verify login failure"):
        driver = step.context.driver
        wait = WebDriverWait(driver, 10)

        # Wait for either error message or alert
        try:
            # Try to find error message on page
            error_element = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            error_text = error_element.text
            step.context.logger.info(f"Login error verified: {error_text}")

            # Attach error message screenshot to Allure
            allure.attach(driver.get_screenshot_as_png(), name=f"Login Error: {error_text}",
                         attachment_type=allure.attachment_type.PNG)

        except:
            # Try to handle alert if present
            try:
                alert = driver.switch_to.alert
                error_text = alert.text
                step.context.logger.info(f"Alert received: {error_text}")
                alert.accept()

                # Attach alert screenshot to Allure
                allure.attach(driver.get_screenshot_as_png(), name=f"Alert: {error_text}",
                             attachment_type=allure.attachment_type.PNG)

            except:
                # If still on login page, check page title
                current_url = driver.current_url
                assert "login" in current_url.lower() or "signin" in current_url.lower(), \
                    f"Expected to remain on login page, but got {current_url}"

                # Attach screenshot showing still on login page
                allure.attach(driver.get_screenshot_as_png(), name="Still on Login Page",
                             attachment_type=allure.attachment_type.PNG)

        shot = take_screenshot(driver, "LOGIN_FAILED_VERIFIED")
        mark_step_screenshot(step, shot)
        mark_step_log(step, step.context.log_path)

        step.context.logger.info("Login failure verified successfully")

