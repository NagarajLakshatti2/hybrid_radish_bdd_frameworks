from cgitb import text

from radish import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import WEB_BASE_URL, WEB_USERNAME, WEB_PASSWORD
from utils.step_wrapper import step_with_screenshot



@given("I open the login page")
def open_login_page(step):
    ogs = getattr(step.context, "step_logs", [])
    step_with_screenshot(
        step,
        "open_login_page",
        lambda: step.context.driver.get(WEB_BASE_URL)
    )



@when("I login with valid credentials")
def login(step):
    def action():
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

    step_with_screenshot(step, "login", action)


@then("I should be logged in")
def verify_login(step):
    def action():
        driver = step.context.driver
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".nav-link"))
        )

    step_with_screenshot(step, "verify_login", action)
