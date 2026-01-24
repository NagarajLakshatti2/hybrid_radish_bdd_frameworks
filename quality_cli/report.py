import subprocess
import os

def generate():
    if not os.path.exists("allure-results"):
        print("⚠ No allure-results found")
        return

    subprocess.run(
        ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
        check=True
    )

    print("📊 Allure report generated at ./allure-report")
