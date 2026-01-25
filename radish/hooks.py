from radish import before, after
from utils.browser import get_web_driver
from utils.screenshot import save_screenshot

import os
import sys

PROJECT_ROOT = os.path.abspath(os.getcwd())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)



@before.each_scenario
def start_browser(scenario, **kwargs):
    scenario.context.driver = get_web_driver()

    scenario_name = scenario.sentence.replace(" ", "_")

    # 📸 Scenario start screenshot
    save_screenshot(
        scenario.context.driver,
        f"scenario_start_{scenario_name}"
    )


@after.each_scenario
def stop_browser(scenario, **kwargs):
    driver = getattr(scenario.context, "driver", None)

    scenario_name = scenario.sentence.replace(" ", "_")

    if driver:
        # 📸 Scenario end screenshot
        save_screenshot(
            driver,
            f"scenario_end_{scenario_name}"
        )
        driver.quit()
