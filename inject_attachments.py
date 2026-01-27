import json
import base64
from pathlib import Path

JSON_FILE = "reports/cucumber.json"
SCREENSHOT_DIR = Path("reports/screenshots")
LOG_DIR = Path("reports/logs")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for feature in data:
    for scenario in feature["elements"]:
        sid = scenario["id"]

        for step in scenario["steps"]:
            if step["result"]["status"] == "failed":
                embeddings = []

                # ---- SCREENSHOT (BASE64) ----
                screenshot = next(
                    SCREENSHOT_DIR.glob(f"FAILED_{sid}_*.png"), None
                )
                if screenshot:
                    embeddings.append({
                        "mime_type": "image/png",
                        "data": base64.b64encode(
                            screenshot.read_bytes()
                        ).decode("utf-8")
                    })

                # ---- LOG FILE (BASE64) ----
                log_file = LOG_DIR / f"scenario_{sid}.log"
                if log_file.exists():
                    embeddings.append({
                        "mime_type": "text/plain",
                        "data": base64.b64encode(
                            log_file.read_bytes()
                        ).decode("utf-8")
                    })

                if embeddings:
                    step["embeddings"] = embeddings

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Screenshot + logs embedded correctly")
