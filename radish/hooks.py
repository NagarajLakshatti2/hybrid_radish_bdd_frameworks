# radish/hooks.py
from radish import before, after

from inject_attachments import inject_attachments
from utils.browser import get_web_driver
from utils.cleanup import clean_previous_artifacts
from utils.screenshot import take_screenshot
from utils.logger import get_scenario_logger
import os


# =========================
# BEFORE ALL
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

    # ✅ ADD THIS LINE (CRITICAL)
    scenario.context.scenario_id = scenario.id

    logger.info(f"START Scenario id={scenario.id}")
    logger.info(f"Log file: {log_path}")


# =========================
# AFTER EACH SCENARIO
# =========================
@after.each_scenario
def after_scenario(scenario):
    logger = scenario.context.logger
    driver = scenario.context.driver

    # ---- Always screenshot ----
    scenario_path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
    scenario_rel = os.path.relpath(scenario_path, "reports")
    logger.info(f"Scenario Screenshot: {scenario_rel}")

    # ---- On failure: inject LINKS into cucumber.json ----
    if scenario.state == "failed":
        fail_path = take_screenshot(driver, f"FAILED_{scenario.id}")
        fail_rel = os.path.relpath(fail_path, "reports")
        log_rel = os.path.relpath(scenario.context.log_path, "reports")

        logger.error(f"FAILED Screenshot: {fail_rel}")

        # ✅ THIS goes into cucumber.json → HTML
        scenario.exception = Exception(
            "FAILED SCENARIO\n\n"
            f"Screenshot:\n{fail_rel}\n\n"
            f"Logs:\n{log_rel}"
        )

    driver.quit()
    logger.info(f"END Scenario id={scenario.id}")

@before.each_step
def before_each_step(step):
    ctx = step.context
    ctx._current_step_index = getattr(ctx, "_current_step_index", -1) + 1

def after_all(features, **kwargs):
    inject_attachments()