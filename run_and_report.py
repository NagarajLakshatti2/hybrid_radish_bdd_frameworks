import subprocess
import sys

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    # 1️⃣ Run Radish (path first – critical)
    run(
        "radish features/web "
        "--tags smoke "
        "--cucumber-json=reports/cucumber.json "
        "--basedir /app"
    )

    # 2️⃣ Inject screenshots + logs
    run("python inject_attachments.py")

    # 3️⃣ Generate HTML report
    run("node cucumber-html.config.js")

    print("\n✅ HTML report generated at reports/html/index.html")

if __name__ == "__main__":
    main()
