from radish import before, after
from utils.browser import get_web_driver
from utils.cleanup import clean_previous_artifacts
from utils.screenshot import take_screenshot
from utils.logger import get_scenario_logger

def before_all(context):
    logger = get_scenario_logger()
    print("before all logger: ", logger.__str__())
    clean_previous_artifacts()

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

    if driver:
        path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
        logger.info(f"Scenario screenshot: {path}")

    if scenario.state == "failed" and driver:
        fail_path = take_screenshot(driver, f"FAILED_{scenario.id}")
        logger.error(f"FAILED screenshot: {fail_path}")

        # 👇 Inject links into failure message
        scenario.exception = Exception(
            f"""
        ❌ Scenario Failed

        📸 Screenshot:
        {fail_path}

        📄 Logs:
        {scenario.context.log_path}
        """
        )

    if driver:
        driver.quit()
