import os
import glob

LOG_DIR = "reports/logs"
SCREENSHOT_DIR = "reports/screenshots"


def clean_previous_artifacts():
    # 🧹 clear scenario logs
    if os.path.exists(LOG_DIR):
        for file in glob.glob(os.path.join(LOG_DIR, "scenario_*.log")):
            os.remove(file)

        # 🧹 clear execution.log (OPTION 3)
        execution_log = os.path.join(LOG_DIR, "execution.log")
        if os.path.exists(execution_log):
            open(execution_log, "w").close()

    # 🧹 clear screenshots
    if os.path.exists(SCREENSHOT_DIR):
        for file in glob.glob(os.path.join(SCREENSHOT_DIR, "*.png")):
            os.remove(file)
