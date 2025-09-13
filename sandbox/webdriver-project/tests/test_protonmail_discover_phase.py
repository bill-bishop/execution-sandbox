import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Ensure the screenshots directory exists
project_dir = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(project_dir, "../screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# Configure WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Debug log file
log_file = os.path.join(screenshots_dir, "protonmail_discover.log")
def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

try:
    log_message("Phase 1: Discover - Test Started: Navigating to ProtonMail")

    # Navigate to ProtonMail
    driver.get("https://proton.me/mail")
    log_message("Page loaded. Capturing interactive elements.")

    # Wait for a moment to ensure elements load
    time.sleep(5)

    # Query all interactive elements
    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")
    inputs = driver.find_elements(By.TAG_NAME, "input")

    # Log buttons
    log_message("Buttons on page:")
    for button in buttons:
        log_message(f"Button Text: '{button.text}' | Selector: {button.get_attribute('outerHTML')}")

    # Log links
    log_message("Links on page:")
    for link in links:
        log_message(f"Link Text: '{link.text}' | Selector: {link.get_attribute('outerHTML')}")

    # Log inputs
    log_message("Inputs on page:")
    for input_field in inputs:
        log_message(f"Input Placeholder: '{input_field.get_attribute('placeholder')}' | Selector: {input_field.get_attribute('outerHTML')}")

    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_discover_phase.png"))
    log_message("Captured screenshot of discover phase.")

    log_message("Phase 1 Completed: Interactive elements logged.")

except Exception as e:
    log_message(f"Phase 1 Failed with Exception: {e}")
    print(f"Phase 1 Failed with Exception: {e}")

finally:
    driver.quit()
    log_message("Phase 1 Finished: WebDriver session closed.")