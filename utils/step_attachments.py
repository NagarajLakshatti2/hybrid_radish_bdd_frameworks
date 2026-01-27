# from pathlib import Path
#
# ATTACHMENTS_DIR = Path("reports/step_attachments")
# ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
#
#
# def register_step_screenshot(step, file_path: str):
#     """
#     Register a screenshot path against this step.
#     """
#     step.context.__dict__.setdefault("_step_screenshots", {})
#     step.context._step_screenshots[id(step)] = file_path
#
#
# def register_step_log(step, log_path: str):
#     """
#     Register a log file against this step.
#     """
#     step.context.__dict__.setdefault("_step_logs", {})
#     step.context._step_logs[id(step)] = log_path
