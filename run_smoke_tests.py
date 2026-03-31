#!/usr/bin/env python3
"""
Script to run Radish BDD tests with @smoke tag and generate Cucumber reports
"""

import os
import sys
import subprocess
import json

def run_smoke_tests():
    """Run login.feature scenarios with @smoke tag"""

    # Change to project directory
    project_dir = r"C:\Users\nagar\gitworkspacebdd\hybrid_radish_bdd_frameworks"
    os.chdir(project_dir)

    print("🚀 Starting Radish BDD Smoke Tests...")
    print("=" * 50)

    # Run radish with smoke tag and cucumber json output
    cmd = [
        "python", "-m", "radish",
        "--tags", "@smoke",
        "--cucumber-json=reports/cucumber.json",
        "features/web/login.feature"
    ]

    print(f"Running command: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")

        if result.returncode == 0:
            print("\n✅ Tests completed successfully!")
            return True
        else:
            print("\n❌ Tests failed!")
            return False

    except subprocess.TimeoutExpired:
        print("\n⏰ Tests timed out after 5 minutes!")
        return False
    except Exception as e:
        print(f"\n💥 Error running tests: {e}")
        return False

def generate_html_report():
    """Generate HTML report from Cucumber JSON"""

    print("\n📊 Generating HTML Report...")
    print("=" * 30)

    # Check if cucumber.json exists
    json_file = "reports/cucumber.json"
    if not os.path.exists(json_file):
        print(f"❌ Cucumber JSON file not found: {json_file}")
        return False

    # Check if cucumber-html.config.js exists
    config_file = "cucumber-html.config.js"
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        return False

    # Run node to generate HTML report
    cmd = ["node", config_file]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        print("Report generation output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        html_file = "reports/html/index.html"
        if os.path.exists(html_file):
            print(f"✅ HTML report generated: {html_file}")
            return True
        else:
            print("❌ HTML report not found after generation")
            return False

    except Exception as e:
        print(f"💥 Error generating report: {e}")
        return False

def open_report():
    """Open the HTML report in browser"""

    html_file = "reports/html/index.html"

    if not os.path.exists(html_file):
        print(f"❌ Report file not found: {html_file}")
        return False

    print(f"\n🌐 Opening report: {html_file}")

    try:
        if sys.platform == "win32":
            os.startfile(html_file)
        else:
            subprocess.run(["xdg-open", html_file])

        print("✅ Report opened in browser!")
        return True

    except Exception as e:
        print(f"💥 Error opening report: {e}")
        return False

def main():
    """Main execution function"""

    print("🔥 Radish BDD Smoke Test Runner")
    print("Date:", "March 31, 2026")
    print("=" * 50)

    # Step 1: Run tests
    test_success = run_smoke_tests()

    if test_success:
        # Step 2: Generate report
        report_success = generate_html_report()

        if report_success:
            # Step 3: Open report
            open_report()
        else:
            print("\n❌ Failed to generate HTML report")
    else:
        print("\n❌ Tests failed, skipping report generation")

    print("\n" + "=" * 50)
    print("🏁 Execution completed!")

if __name__ == "__main__":
    main()
