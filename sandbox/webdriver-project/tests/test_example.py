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
    # Open a test webpage
    driver.get("https://example.com")

    # Wait for the page to load
    time.sleep(2)

    # Capture a screenshot
    screenshot_path = "../screenshots/example_test.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at {screenshot_path}")

    # Check page title
    assert "Example Domain" in driver.title
    print("Test Passed: Page title is correct.")

except Exception as e:
    print(f"Test Failed with Exception: {e}")

finally:
    driver.quit()