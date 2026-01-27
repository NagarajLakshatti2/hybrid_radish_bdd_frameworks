import json
import base64
from pathlib import Path

JSON_FILE = "reports/cucumber.json"
SCREENSHOT_DIR = Path("reports/screenshots")
LOG_DIR = Path("reports/logs")


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


for feature in data:
    for scenario in feature.get("elements", []):
        sid = scenario["id"]

        scenario_log = LOG_DIR / f"scenario_{sid}.log"
        scenario_logs_b64 = (
            b64(scenario_log) if scenario_log.exists() else None
        )

        for step in scenario.get("steps", []):
            status = step["result"]["status"]

            embeddings = []

            # ============================
            # SCREENSHOT (PASS + FAIL)
            # ============================
            shot = next(
                SCREENSHOT_DIR.glob(f"*_{sid}_*.png"),
                None
            )
            if shot:
                embeddings.append({
                    "mime_type": "image/png",
                    "data": b64(shot)
                })

            # ============================
            # LOG FILE (PASS + FAIL)
            # ============================
            if scenario_logs_b64:
                embeddings.append({
                    "mime_type": "text/plain",
                    "data": scenario_logs_b64
                })

            # ============================
            # ATTACH ONLY IF EXISTS
            # ============================
            if embeddings:
                step["embeddings"] = embeddings


with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ PASS + FAIL step screenshots & logs embedded")
