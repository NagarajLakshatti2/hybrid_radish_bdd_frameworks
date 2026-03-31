from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging


class BasePage:
    """
    Base class for all page objects.
    Provides common methods and utilities for all pages.
    """

    def __init__(self, driver, timeout=10, logger=None):
        """
        Initialize base page

        Args:
            driver: Selenium WebDriver instance
            timeout: Default wait timeout in seconds
            logger: Logger instance for logging actions
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

    # ============= ELEMENT INTERACTION METHODS =============

    def click(self, locator):
        """Click on an element with explicit wait for clickability"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked on element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {str(e)}")
            raise

    def enter_text(self, locator, text):
        """Clear field and enter text with explicit wait for visibility"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text in element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to enter text in {locator}: {str(e)}")
            raise

    def get_text(self, locator):
        """Get text from element with explicit wait"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Retrieved text from element: {locator} = '{text}'")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from {locator}: {str(e)}")
            raise

    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element {locator} is visible")
            return True
        except:
            self.logger.warning(f"Element {locator} is not visible")
            return False

    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            self.logger.info(f"Element {locator} is present")
            return True
        except:
            self.logger.warning(f"Element {locator} not found")
            return False

    def wait_for_element(self, locator):
        """Backward compatibility: wait for element visibility"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_visible(self, locator, timeout=None):
        """Explicit wait for element visibility"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element {locator} is now visible")
            return element
        except Exception as e:
            self.logger.error(f"Timeout waiting for element {locator}: {str(e)}")
            raise

    def wait_for_element_clickable(self, locator, timeout=None):
        """Explicit wait for element to be clickable"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.info(f"Element {locator} is now clickable")
            return element
        except Exception as e:
            self.logger.error(f"Timeout waiting for clickable element {locator}: {str(e)}")
            raise

    # ============= ASSERTION METHODS =============

    def assert_element_visible(self, locator, message=None):
        """Assert that element is visible"""
        msg = message or f"Element {locator} is not visible"
        assert self.is_element_visible(locator), msg
        self.logger.info(f"✓ Assertion passed: {msg}")

    def assert_text_in_element(self, locator, expected_text, message=None):
        """Assert that expected text is in element"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            actual_text = element.text
            msg = message or f"Expected '{expected_text}' in '{actual_text}'"
            assert expected_text in actual_text, msg
            self.logger.info(f"✓ Assertion passed: {msg}")
        except AssertionError:
            self.logger.error(f"✗ Assertion failed: {msg}")
            raise

    def assert_text_equals(self, locator, expected_text, message=None):
        """Assert that element text equals expected text"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            actual_text = element.text
            msg = message or f"Expected text '{expected_text}' but got '{actual_text}'"
            assert actual_text == expected_text, msg
            self.logger.info(f"✓ Assertion passed: {msg}")
        except AssertionError:
            self.logger.error(f"✗ Assertion failed: {msg}")
            raise

    # ============= PAGE NAVIGATION =============

    def go_to_url(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def get_current_url(self):
        """Get current page URL"""
        url = self.driver.current_url
        self.logger.info(f"Current URL: {url}")
        return url

    def get_page_title(self):
        """Get page title"""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title

    # ============= COMMON UTILITIES =============

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")

    def get_element_attribute(self, locator, attribute):
        """Get element attribute value"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            value = element.get_attribute(attribute)
            self.logger.info(f"Element {locator} attribute '{attribute}' = '{value}'")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get attribute from {locator}: {str(e)}")
            raise
