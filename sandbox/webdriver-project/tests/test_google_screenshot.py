from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Configure WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open Google
    driver.get("https://www.google.com")

    # Wait for the page to load
    time.sleep(2)

    # Capture a screenshot
    screenshot_path = "../screenshots/google_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at {screenshot_path}")

except Exception as e:
    print(f"Test Failed with Exception: {e}")

finally:
    driver.quit()