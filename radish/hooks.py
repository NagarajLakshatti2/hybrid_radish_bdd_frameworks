from radish import before, after
from utils.browser import get_web_driver


@before.each_scenario
def start_browser(scenario, **kwargs):
    scenario.context.driver = get_web_driver()


@after.each_scenario
def stop_browser(scenario, **kwargs):
    driver = getattr(scenario.context, "driver", None)

    if driver:
        try:
            driver.quit()
        except Exception:
            pass
