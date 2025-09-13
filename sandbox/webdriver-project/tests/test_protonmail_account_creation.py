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
log_file = os.path.join(screenshots_dir, "protonmail_account_creation.log")
def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

try:
    log_message("Account Creation Test Started: Navigating to ProtonMail")

    # Navigate to ProtonMail
    driver.get("https://proton.me/mail")
    log_message("Page loaded. Looking for the 'Create a free account' button.")

    # Wait for the page to load
    time.sleep(5)

    # Locate the "Create a free account" button
    create_account_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Create a free account')]")
    log_message("'Create a free account' button found. Clicking it.")

    # Click the button
    create_account_button.click()
    log_message("Clicked 'Create a free account' button. Waiting for navigation.")

    # Wait for navigation to the account creation page
    time.sleep(5)

    # Take a screenshot of the account creation page
    account_creation_screenshot = os.path.join(screenshots_dir, "protonmail_account_creation_page.png")
    driver.save_screenshot(account_creation_screenshot)
    log_message(f"Screenshot of account creation page saved: {account_creation_screenshot}")

    # Validate navigation by checking the presence of the signup form
    signup_form = driver.find_element(By.XPATH, "//form[contains(@action, 'signup')]")
    log_message("Signup form found. Account creation page loaded successfully.")

except Exception as e:
    log_message(f"Account Creation Test Failed with Exception: {e}")
    print(f"Account Creation Test Failed with Exception: {e}")

finally:
    driver.quit()
    log_message("Account Creation Test Finished: WebDriver session closed.")