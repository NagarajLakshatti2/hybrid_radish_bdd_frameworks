from radish import before, after
from utils.browser import get_web_driver
from utils.screenshot import take_screenshot, attach_screenshot_to_step
from utils.logger import logger   # 👈 import the logger object

@before.each_scenario
def start_browser(scenario, **kwargs):
    # ✅ attach logger to context
    scenario.context.logger = logger

    # ✅ attach logger to context
    scenario.context.logger = logger
    scenario.context.driver = get_web_driver()

@after.each_scenario
def after_scenario(scenario, **kwargs):
    logger = scenario.context.logger
    driver = getattr(scenario.context, "driver", None)

    if driver:
        # always screenshot (PASS + FAIL)
        path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
        logger.info(f"Scenario screenshot: {path}")

    if scenario.state == "failed" and driver:
        fail_path = take_screenshot(driver, f"FAILED_{scenario.id}")
        logger.error(f"FAILED screenshot: {fail_path}")

    logger.info("Scenario ended")


@after.each_scenario
def stop_browser(scenario, **kwargs):
    scenario.context.logger.info("Scenario started")
    driver = getattr(scenario.context, "driver", None)
    if driver:
        driver.quit()


