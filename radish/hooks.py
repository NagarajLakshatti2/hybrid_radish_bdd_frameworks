from radish import before, after
from utils.browser import get_web_driver
from utils.screenshot import take_screenshot
from utils.logger import get_scenario_logger


@before.each_scenario
def start_browser(scenario):
    logger, log_path = get_scenario_logger(scenario.id)

    scenario.context.logger = logger
    scenario.context.log_path = log_path
    scenario.context.driver = get_web_driver()

    logger.info(f"START Scenario id={scenario.id}")
    logger.info(f"Log file: {log_path}")


@after.each_scenario
def after_scenario(scenario):
    logger = scenario.context.logger
    driver = getattr(scenario.context, "driver", None)

    # ✅ screenshot always
    if driver:
        path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
        logger.info(f"Scenario screenshot: {path}")

    # ❌ failed case
    if scenario.state == "failed" and driver:
        fail_path = take_screenshot(driver, f"FAILED_{scenario.id}")
        logger.error(f"FAILED screenshot: {fail_path}")

        # 👇 appears in Cucumber report (clickable)
        scenario.result.error = (
            f"\n--- DEBUG INFO ---\n"
            f"Screenshot: {fail_path}\n"
            f"Log file : {scenario.context.log_path}\n"
        )

    logger.info(f"END Scenario id={scenario.id}")

    if driver:
        driver.quit()
