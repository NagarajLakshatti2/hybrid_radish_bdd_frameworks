import os


def write_allure_environment():
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write("Project=Hybrid Radish BDD Framework\n")
        f.write("Module=Web\n")
        f.write("Browser=Chrome\n")
        f.write("Execution=Local\n")
        f.write("OS=Windows\n")
        f.write("Execution By=Nagaraj Lakshatti\n")