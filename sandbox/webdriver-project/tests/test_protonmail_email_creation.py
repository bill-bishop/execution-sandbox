import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
log_file = os.path.join(screenshots_dir, "protonmail_debug.log")
def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

try:
    log_message("Test Started: Navigating to ProtonMail")

    # Navigate to ProtonMail
    driver.get("https://proton.me/mail")
    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_home.png"))
    log_message("Step 1: Captured screenshot after navigating to ProtonMail home page.")

    # Click the "Create a free account" link
    create_account_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Create a free account"))
    )
    create_account_link.click()
    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_signup_page.png"))
    log_message("Step 2: Clicked 'Create a free account' and navigated to signup page.")

    # Wait for the signup form to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    log_message("Step 3: Signup form loaded.")

    # Fill in the form fields (example data)
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("testuser12345")
    log_message("Step 4: Entered username.")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("TestPassword123!")
    log_message("Step 5: Entered password.")

    confirm_password_field = driver.find_element(By.ID, "passwordc")
    confirm_password_field.send_keys("TestPassword123!")
    log_message("Step 6: Confirmed password.")

    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_form_filled.png"))
    log_message("Step 7: Filled form fields and captured screenshot.")

    # Submit the form
    create_account_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    create_account_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.success")))
    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_account_created.png"))
    log_message("Step 8: Submitted the form and captured screenshot.")

    log_message("Test Completed: Email account creation process simulated.")

except Exception as e:
    log_message(f"Test Failed with Exception: {e}")
    with open(os.path.join(screenshots_dir, "protonmail_error_page.html"), "w") as f:
        f.write(driver.page_source)
    driver.save_screenshot(os.path.join(screenshots_dir, "protonmail_error.png"))
    log_message("Captured error page screenshot and HTML.")
    print(f"Test Failed with Exception: {e}")

finally:
    driver.quit()
    log_message("Test Finished: WebDriver session closed.")