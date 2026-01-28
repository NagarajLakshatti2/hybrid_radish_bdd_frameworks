const reporter = require("cucumber-html-reporter");

const options = {
  theme: "bootstrap",
  jsonFile: "reports/cucumber.json",
  output: "reports/html/index.html",
  reportSuiteAsScenarios: true,
  scenarioTimestamp: true,
  launchReport: false,
  metadata: {
    "Test Framework": "Radish BDD",
    "Language": "Python",
    "Browser": "Chrome",
    "Platform": "GitHub Pages"
  }
};

reporter.generate(options);
