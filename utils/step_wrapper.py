from utils.screenshot import save_screenshot


def step_with_screenshot(step, step_name, action):
    driver = step.context.driver

    try:
        action()
        screenshot = save_screenshot(driver, f"step_{step_name}")
        step.context.last_screenshot = screenshot

    except Exception as e:
        screenshot = save_screenshot(driver, f"FAILED_{step_name}")

        raise AssertionError(
            f"Step failed: {step_name}\nScreenshot: {screenshot}"
        ) from e
