from radish import before, after
from utils.browser import get_web_driver
from utils.cleanup import clean_previous_artifacts
from utils.screenshot import take_screenshot
from utils.logger import get_scenario_logger


# =========================
# BEFORE ALL (ONE TIME)
# =========================
@before.all
def before_all(features, **kwargs):
    clean_previous_artifacts()


# =========================
# BEFORE EACH SCENARIO
# =========================
@before.each_scenario
def start_browser(scenario):
    logger, log_path = get_scenario_logger(scenario.id)

    scenario.context.logger = logger
    scenario.context.log_path = log_path
    scenario.context.driver = get_web_driver()

    logger.info(f"START Scenario id={scenario.id}")
    logger.info(f"Log file: {log_path}")


# =========================
# AFTER EACH SCENARIO
# =========================
@after.each_scenario
def after_scenario(scenario):
    logger = scenario.context.logger
    driver = getattr(scenario.context, "driver", None)

    # ---------- Always take scenario screenshot ----------
    if driver:
        scenario_path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
        scenario_rel = scenario_path.replace("reports/", "")
        logger.info(f"Scenario Screenshot: {scenario_rel}")

    # ---------- On failure ----------
    if scenario.state == "failed" and driver:
        fail_path = take_screenshot(driver, f"FAILED_{scenario.id}")
        fail_rel = fail_path.replace("reports/", "")
        log_rel = scenario.context.log_path.replace("reports/", "")

        logger.error(f"FAILED Screenshot: {fail_rel}")

        # 👇 This text appears INSIDE Cucumber HTML
        scenario.exception = Exception(
            f"""
        FAILED SCENARIO

        Screenshot: reports/screenshots/FAILED_{scenario.id}.png
        Logs: reports/logs/scenario_{scenario.id}.log
        """
        )


    if driver:
        driver.quit()
