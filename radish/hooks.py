
from radish import before, after, world, scenario

from utils.allure_env import write_allure_environment
from utils.browser import get_web_driver
from utils.screenshot import attach_screenshot, save_screenshot


@before.all
def setup_allure_environment(features, **kwargs):
    write_allure_environment()

@before.each_scenario
def start_browser(scenario, **kwargs):
    scenario.context.driver = get_web_driver()

@after.each_scenario
def stop_browser(scenario, **kwargs):
    driver = getattr(scenario.context, "driver", None)

    # Best-effort screenshot
    try:
        if driver:
            save_screenshot(driver, scenario.name)
    except Exception:
        pass

    if driver:
        driver.quit()