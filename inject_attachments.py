import json
import base64
import os
from pathlib import Path

JSON_FILE = Path("reports/cucumber.json")
SCREENSHOT_DIR = Path("reports/screenshots")
LOG_DIR = Path("reports/logs")


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def inject_attachments():
    if not JSON_FILE.exists():
        print("⚠️ cucumber.json not found, skipping attachment injection")
        return

    with JSON_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for feature in data:
        for scenario in feature.get("elements", []):
            sid = scenario.get("id")
            if not sid:
                continue

            scenario_log = LOG_DIR / f"scenario_{sid}.log"
            scenario_log_b64 = (
                b64(scenario_log) if scenario_log.exists() else None
            )

            screenshots = list(
                SCREENSHOT_DIR.glob(f"*_{sid}_*.png")
            )

            for step in scenario.get("steps", []):
                embeddings = []

                # Attach screenshots
                for shot in screenshots:
                    embeddings.append({
                        "mime_type": "image/png",
                        "data": b64(shot)
                    })

                # Attach log
                if scenario_log_b64:
                    embeddings.append({
                        "mime_type": "text/plain",
                        "data": scenario_log_b64
                    })

                if embeddings:
                    step["embeddings"] = embeddings

    with JSON_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ PASS + FAIL step screenshots & logs embedded")

if __name__ == "__main__":
    inject_attachments()
