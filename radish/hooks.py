from radish import before, after
from utils.browser import get_web_driver
from utils.screenshot import take_screenshot, attach_screenshot_to_step
from utils.logger import log_info, log_error



@before.each_scenario
def start_browser(scenario, **kwargs):
    scenario.context.driver = get_web_driver()
    log_info(f"Starting scenario: [id={scenario.id}]")


@after.each_scenario
def stop_browser(scenario, **kwargs):
    log_info(f"Ending scenario: [id={scenario.id}]")
    driver = getattr(scenario.context, "driver", None)
    if driver:
        driver.quit()


@after.each_scenario
def screenshot_on_failure(scenario):
    if scenario.state == "failed":
        log_error(f"Scenario FAILED: [id={scenario.id}]")

        driver = getattr(scenario.context, "driver", None)
        if driver:
            path = take_screenshot(driver, "FAILED")
            if path:
                log_info(f"Screenshot saved: {path}")


@after.each_scenario
def screenshot_after_scenario(scenario):
    driver = getattr(scenario.context, "driver", None)
    if not driver:
        return

    path = take_screenshot(driver, f"SCENARIO_{scenario.id}")
    if path:
        scenario.attach(
            open(path, "rb").read(),
            mime_type="image/png",
            description="Scenario Screenshot"
        )

