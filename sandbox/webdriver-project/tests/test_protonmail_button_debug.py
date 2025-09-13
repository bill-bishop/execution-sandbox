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

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Debug log file
log_file = os.path.join(screenshots_dir, "protonmail_button_debug_clean.log")
def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

try:
    log_message("Test Started: Navigating to ProtonMail")

    # Navigate to ProtonMail
    driver.get("https://proton.me/mail")
    log_message("Page loaded.")

    # Wait for a moment to ensure elements load
    time.sleep(5)

    # Query for all buttons and links
    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")

    # Log button text
    log_message("Found Buttons:")
    for button in buttons:
        log_message(f"Button Text: {button.text}")

    # Log link text
    log_message("Found Links:")
    for link in links:
        log_message(f"Link Text: {link.text}")

    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_debug_buttons_clean.png"))
    log_message("Captured screenshot after querying interactive elements.")

    log_message("Test Completed.")

except Exception as e:
    log_message(f"Test Failed with Exception: {e}")
    print(f"Test Failed with Exception: {e}")

finally:
    driver.quit()
    log_message("Test Finished: WebDriver session closed.")