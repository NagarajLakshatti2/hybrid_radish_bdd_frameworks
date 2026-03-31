#!/usr/bin/env python3
"""
Official Cucumber HTML Report Generator
Generates reports that look like the official Cucumber reports from reports.cucumber.io
"""

import os
import sys
import json
from datetime import datetime

def generate_official_cucumber_report():
    """Generate official Cucumber HTML report"""

    project_dir = r"C:\Users\nagar\gitworkspacebdd\hybrid_radish_bdd_frameworks"
    os.chdir(project_dir)

    print("🥒 Generating Official Cucumber HTML Report...")
    print("=" * 60)

    # Check if cucumber.json exists
    cucumber_json = "reports/cucumber.json"
    if not os.path.exists(cucumber_json):
        print(f"❌ Cucumber JSON file not found: {cucumber_json}")
        print("Please run tests first to generate cucumber.json")
        return False

    # Generate official-style HTML directly with Python
    print("Generating official Cucumber report with Python...")
    return generate_alternative_official_report()

def generate_alternative_official_report():
    """Generate an alternative official-looking Cucumber report"""

    print("🔄 Generating alternative official Cucumber report...")

    try:
        # Read cucumber JSON
        with open("reports/cucumber.json", 'r', encoding='utf-8') as f:
            cucumber_data = json.load(f)

        # Generate official-style HTML
        html_content = generate_official_html(cucumber_data)

        # Write the report
        output_file = "reports/html/cucumber-official-report.html"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Alternative official report generated: {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error generating alternative report: {e}")
        return False

def generate_official_html(cucumber_data):
    """Generate HTML that looks like official Cucumber reports"""

    # Calculate statistics
    total_scenarios = 0
    passed_scenarios = 0
    failed_scenarios = 0
    total_steps = 0
    passed_steps = 0
    failed_steps = 0
    total_duration = 0

    features = []

    for feature_data in cucumber_data:
        feature = {
            'name': feature_data.get('name', 'Unnamed Feature'),
            'scenarios': []
        }

        for element in feature_data.get('elements', []):
            if element.get('type') == 'scenario':
                scenario = {
                    'name': element.get('name', ''),
                    'tags': [tag['name'] for tag in element.get('tags', [])],
                    'status': 'passed',
                    'duration': 0,
                    'steps': []
                }

                # Process steps
                for step in element.get('steps', []):
                    step_result = step.get('result', {})
                    step_status = step_result.get('status', 'unknown')
                    step_duration = step_result.get('duration', 0)

                    scenario['steps'].append({
                        'keyword': step.get('keyword', ''),
                        'name': step.get('name', ''),
                        'status': step_status,
                        'duration': step_duration / 1000000000 if step_duration else 0
                    })

                    scenario['duration'] += step_duration / 1000000000 if step_duration else 0

                    if step_status != 'passed':
                        scenario['status'] = 'failed'

                feature['scenarios'].append(scenario)

                # Update totals
                total_scenarios += 1
                if scenario['status'] == 'passed':
                    passed_scenarios += 1
                else:
                    failed_scenarios += 1

                total_steps += len(scenario['steps'])
                passed_steps += sum(1 for s in scenario['steps'] if s['status'] == 'passed')
                failed_steps += sum(1 for s in scenario['steps'] if s['status'] != 'passed')
                total_duration += scenario['duration']

        if feature['scenarios']:
            features.append(feature)

    # Build HTML using string formatting instead of f-strings
    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html>
<head>
    <title>Cucumber Reports - Official Style</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .summary-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric {
            text-align: center;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            display: block;
        }
        .metric-label {
            color: #6c757d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .passed { color: #28a745; }
        .failed { color: #dc3545; }
        .total { color: #007bff; }
        .feature {
            background: white;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .feature-header {
            background: #f8f9fa;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #dee2e6;
            border-radius: 8px 8px 0 0;
        }
        .feature-title {
            margin: 0;
            font-size: 1.25rem;
            font-weight: 600;
            color: #495057;
        }
        .scenario {
            border-bottom: 1px solid #f1f3f4;
        }
        .scenario:last-child {
            border-bottom: none;
        }
        .scenario-header {
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #fff;
        }
        .scenario-title {
            font-weight: 500;
            color: #495057;
        }
        .scenario-status {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
        }
        .status-passed {
            background: #d4edda;
            color: #155724;
        }
        .status-failed {
            background: #f8d7da;
            color: #721c24;
        }
        .scenario-duration {
            color: #6c757d;
            font-size: 0.875rem;
        }
        .steps {
            padding: 0 1.5rem 1rem 1.5rem;
        }
        .step {
            padding: 0.5rem 0;
            display: flex;
            align-items: center;
        }
        .step-keyword {
            font-weight: bold;
            color: #007bff;
            min-width: 70px;
            font-size: 0.9rem;
        }
        .step-name {
            flex: 1;
            color: #495057;
        }
        .step-status {
            padding: 0.125rem 0.5rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
        }
        .step-passed {
            background: #d4edda;
            color: #155724;
        }
        .step-failed {
            background: #f8d7da;
            color: #721c24;
        }
        .step-duration {
            color: #6c757d;
            font-size: 0.8rem;
            margin-left: 1rem;
        }
        .tags {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .tag {
            background: #e9ecef;
            color: #495057;
            padding: 0.125rem 0.5rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .footer {
            text-align: center;
            padding: 2rem;
            color: #6c757d;
            background: white;
            margin-top: 2rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <h1 class="display-4">🥒 Cucumber Test Reports</h1>
                    <p class="lead">Official Style - Generated on """)

    html_parts.append(datetime.now().strftime('%B %d, %Y at %I:%M %p'))
    html_parts.append("""</p>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Summary Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="summary-card">
                    <div class="metric">
                        <span class="metric-value total">""")
    html_parts.append(str(total_scenarios))
    html_parts.append("""</span>
                        <span class="metric-label">Scenarios</span>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="summary-card">
                    <div class="metric">
                        <span class="metric-value passed">""")
    html_parts.append(str(passed_scenarios))
    html_parts.append("""</span>
                        <span class="metric-label">Passed</span>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="summary-card">
                    <div class="metric">
                        <span class="metric-value failed">""")
    html_parts.append(str(failed_scenarios))
    html_parts.append("""</span>
                        <span class="metric-label">Failed</span>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="summary-card">
                    <div class="metric">
                        <span class="metric-value total">""")
    html_parts.append("{:.1f}".format(total_duration))
    html_parts.append("""s</span>
                        <span class="metric-label">Duration</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Features -->""")

    for feature in features:
        html_parts.append("""
        <div class="feature">
            <div class="feature-header">
                <h2 class="feature-title">""")
        html_parts.append(feature["name"])
        html_parts.append("""</h2>
            </div>""")

        for scenario in feature["scenarios"]:
            html_parts.append("""
            <div class="scenario">
                <div class="scenario-header">
                    <div>
                        <h4 class="scenario-title">""")
            html_parts.append(scenario["name"])
            html_parts.append("""</h4>
                        <div class="tags">""")

            for tag in scenario["tags"]:
                html_parts.append('<span class="tag">')
                html_parts.append(tag)
                html_parts.append('</span>')

            html_parts.append("""
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="scenario-status status-""")
            html_parts.append(scenario["status"])
            html_parts.append('">')
            html_parts.append(scenario["status"])
            html_parts.append("""</span>
                        <div class="scenario-duration">""")
            html_parts.append("{:.2f}".format(scenario["duration"]))
            html_parts.append("""s</div>
                    </div>
                </div>
                <div class="steps">""")

            for step in scenario["steps"]:
                html_parts.append("""
                    <div class="step">
                        <span class="step-keyword">""")
                html_parts.append(step["keyword"])
                html_parts.append("""</span>
                        <span class="step-name">""")
                html_parts.append(step["name"])
                html_parts.append("""</span>
                        <span class="step-status step-""")
                html_parts.append(step["status"])
                html_parts.append('">')
                html_parts.append(step["status"])
                html_parts.append("""</span>
                        <span class="step-duration">""")
                html_parts.append("{:.2f}".format(step["duration"]))
                html_parts.append("""s</span>
                    </div>""")

            html_parts.append("""
                </div>
            </div>""")

        html_parts.append("""
        </div>""")

    html_parts.append("""
    </div>

    <div class="footer">
        <div class="container">
            <p><strong>Cucumber BDD Framework</strong> - Official Report Style</p>
            <p>Generated by Radish BDD | Framework: Python | Reports: Official Cucumber Style</p>
            <p>&copy; 2024 - Professional Test Automation Reports</p>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>""")

    return ''.join(html_parts)

def open_official_report_in_chrome():
    """Open the official Cucumber report in Chrome"""

    possible_reports = [
        "reports/html/cucumber-official-report.html",
        "reports/html/cucumber-report.html",
        "reports/html/index.html"
    ]

    html_file = None
    for report_path in possible_reports:
        if os.path.exists(report_path):
            html_file = report_path
            break

    if not html_file:
        print("❌ No official report file found")
        return False

    print(f"🌐 Opening Official Cucumber Report in Chrome: {html_file}")

    try:
        # Convert to file:// URL
        file_url = f"file:///{os.path.abspath(html_file).replace(chr(92), '/')}"

        # Try different Chrome paths
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "chrome.exe"
        ]

        for chrome_path in chrome_paths:
            try:
                if chrome_path == "chrome.exe":
                    os.system(f'start chrome "{file_url}"')
                else:
                    os.system(f'"{chrome_path}" "{file_url}"')

                print("✅ Official Cucumber report opened in Chrome!")
                return True
            except:
                continue

        # Fallback to default browser
        os.startfile(html_file)
        print("✅ Report opened in default browser!")
        return True

    except Exception as e:
        print(f"💥 Error opening report: {e}")
        return False

def main():
    """Main execution function"""

    print("🚀 Official Cucumber Report Generator")
    print("Date:", "March 31, 2026")
    print("=" * 60)

    # Generate official report
    report_success = generate_official_cucumber_report()

    if report_success:
        print("\n🔥 Opening official report in Chrome...")
        open_success = open_official_report_in_chrome()

        if open_success:
            print("✅ Complete success! Official Cucumber report generated and opened in Chrome.")
        else:
            print("⚠️ Report generated but could not open in Chrome.")
    else:
        print("❌ Failed to generate official report")

    print("\n" + "=" * 60)
    print("🏁 Official Cucumber report generation completed!")

    print("\n📋 Official Report Features:")
    print("- 🥒 Authentic Cucumber report styling")
    print("- 📊 Professional dashboard layout")
    print("- 🏷️ Feature and scenario organization")
    print("- 📈 Official Cucumber metrics display")
    print("- 🎨 Bootstrap 4 responsive design")
    print("- 🌐 Matches reports.cucumber.io style")

if __name__ == "__main__":
    main()

