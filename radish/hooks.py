# radish/hooks.py
from radish import before, after
from utils.browser import get_web_driver
from utils.cleanup import clean_previous_artifacts
from utils.screenshot import take_screenshot
from utils.logger import get_scenario_logger
import os
import time
import allure  # Add Allure import


# =========================
# BEFORE ALL
# =========================
@before.all
def before_all(features, **kwargs):
    """Execute before all test features"""
    clean_previous_artifacts()
    print("=" * 70)
    print("[START] TEST EXECUTION STARTED")
    print("=" * 70)

    # Allure environment setup via environment variables
    import os
    os.environ['ALLURE_TEST_ENVIRONMENT'] = 'Radish BDD'
    os.environ['ALLURE_TEST_FRAMEWORK'] = 'Radish BDD'
    os.environ['ALLURE_TEST_LANGUAGE'] = 'Python'
    os.environ['ALLURE_TEST_BROWSER'] = 'Chrome'
    os.environ['ALLURE_TEST_PLATFORM'] = 'Windows'


# =========================
# AFTER ALL
# =========================
@after.all
def after_all(features, **kwargs):
    """Execute after all test features - generate summary"""
    print("=" * 70)
    print("[PASS] TEST EXECUTION COMPLETED")
    print("=" * 70)


# =========================
# BEFORE EACH SCENARIO
# =========================
@before.each_scenario
def start_browser(scenario):
    """Setup browser and context before each scenario"""
    logger, log_path = get_scenario_logger(scenario.id)

    scenario.context.logger = logger
    scenario.context.log_path = log_path
    scenario.context.driver = get_web_driver()
    scenario.context.scenario_id = scenario.id
    scenario.context.scenario_start_time = time.time()

    # Allure scenario setup
    scenario_name = getattr(scenario, 'name', f'Scenario {scenario.id}')
    allure.dynamic.title(scenario_name)
    allure.dynamic.description(f"Login functionality test scenario")
    allure.dynamic.severity(allure.severity_level.NORMAL)
    allure.dynamic.feature("Login Feature")
    allure.dynamic.story("User Authentication")

    logger.info("=" * 70)
    logger.info(f"[START] SCENARIO: {scenario_name}")
    logger.info(f"   Scenario ID: {scenario.id}")
    logger.info(f"   Log file: {log_path}")
    logger.info("=" * 70)


# =========================
# AFTER EACH SCENARIO
# =========================
@after.each_scenario
def after_scenario(scenario):
    """Cleanup and capture artifacts after each scenario"""
    logger = scenario.context.logger
    driver = scenario.context.driver

    # Calculate scenario duration
    if hasattr(scenario.context, 'scenario_start_time'):
        duration = time.time() - scenario.context.scenario_start_time
        logger.info(f"[TIME] Duration: {duration:.2f}s")

    # ---- Always screenshot ----
    scenario_path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
    scenario_rel = os.path.relpath(scenario_path, "reports")
    logger.info(f"[SCREENSHOT] Scenario Screenshot: {scenario_rel}")

    # Allure attachments - Always attach scenario screenshot
    allure.attach.file(scenario_path, name=f"Scenario {scenario.id} Screenshot",
                      attachment_type=allure.attachment_type.PNG)

    # Attach logs to Allure
    if os.path.exists(scenario.context.log_path):
        with open(scenario.context.log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        allure.attach(log_content, name=f"Scenario {scenario.id} Logs",
                     attachment_type=allure.attachment_type.TEXT)

    # ---- On failure: additional attachments ----
    if scenario.state == "failed":
        fail_path = take_screenshot(driver, f"FAILED_{scenario.id}")
        fail_rel = os.path.relpath(fail_path, "reports")
        log_rel = os.path.relpath(scenario.context.log_path, "reports")

        logger.error(f"[FAILED] Screenshot: {fail_rel}")

        # Allure failure attachments
        allure.attach.file(fail_path, name=f"Failure Screenshot - Scenario {scenario.id}",
                          attachment_type=allure.attachment_type.PNG)

        # Inject into cucumber.json for HTML reports
        scenario.exception = Exception(
            "FAILED SCENARIO\n\n"
            f"Screenshot:\n{fail_rel}\n\n"
            f"Logs:\n{log_rel}"
        )
    else:
        logger.info(f"[PASS] PASSED")

    driver.quit()
    scenario_name = getattr(scenario, 'name', f'Scenario {scenario.id}')
    logger.info(f"[END] SCENARIO: {scenario_name}")
    logger.info("=" * 70)


# =========================
# BEFORE EACH STEP
# =========================
@before.each_step
def before_step(step):
    """Log step information before execution"""
    ctx = step.context
    ctx._current_step_index = getattr(ctx, "_current_step_index", -1) + 1

    logger = ctx.logger
    logger.debug(f"▶️  Step {ctx._current_step_index}: {step.text}")


# =========================
# AFTER EACH STEP
# =========================
@after.each_step
def after_step(step):
    """Capture step details after execution"""
    logger = step.context.logger
    ctx = step.context
    step_index = ctx._current_step_index

    if step.state == "passed":
        logger.debug(f"✓ Step {step_index} PASSED")
    elif step.state == "failed":
        logger.error(f"✗ Step {step_index} FAILED: {step.text}")

        # Auto-capture failure screenshot
        if hasattr(ctx, 'driver') and ctx.driver:
            try:
                screenshot_path = take_screenshot(
                    ctx.driver,
                    f"STEP_FAILURE_{step_index}_{step.id}"
                )
                logger.error(f"   Screenshot: {screenshot_path}")
            except Exception as e:
                logger.error(f"   Failed to capture screenshot: {str(e)}")
    elif step.state == "skipped":
        logger.warning(f"⊘ Step {step_index} SKIPPED")
