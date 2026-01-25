import os
import glob
import xml.etree.ElementTree as ET

JUNIT_XML = "reports/junit-web.xml"
SCREENSHOT_DIR = "reports/screenshots"
OUTPUT_XML = "reports/junit-web-with-screenshots.xml"


def inject_screenshots():
    tree = ET.parse(JUNIT_XML)
    root = tree.getroot()

    for testcase in root.iter("testcase"):
        scenario_name = testcase.attrib.get("name", "").replace(" ", "_")

        screenshots = glob.glob(
            f"{SCREENSHOT_DIR}/*{scenario_name}*.png"
        )

        if screenshots:
            system_out = ET.SubElement(testcase, "system-out")
            system_out.text = "\n".join(screenshots)

    tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
    print(f"✅ JUnit with screenshots created: {OUTPUT_XML}")


if __name__ == "__main__":
    inject_screenshots()
