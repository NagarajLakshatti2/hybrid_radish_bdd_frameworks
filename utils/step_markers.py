from pathlib import Path

MARKERS_DIR = Path("reports/step_markers")
MARKERS_DIR.mkdir(parents=True, exist_ok=True)

def mark_step_screenshot(step, screenshot_path: str):
    scenario_id = step.context.scenario_id
    step_index = step.context._current_step_index

    marker = MARKERS_DIR / f"{scenario_id}_{step_index}.screenshot"
    marker.write_text(screenshot_path)

def mark_step_log(step, log_path: str):
    scenario_id = step.context.scenario_id
    step_index = step.context._current_step_index

    marker = MARKERS_DIR / f"{scenario_id}_{step_index}.log"
    marker.write_text(log_path)
