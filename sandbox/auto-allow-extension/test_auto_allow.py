from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--load-extension=/sandbox/auto-allow-extension")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--remote-debugging-port=9222")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the test HTML file
    driver.get("file:///sandbox/auto-allow-extension/test-confirm-trigger.html")

    # Wait for the extension to interact
    time.sleep(5)

    # Take a screenshot to validate UI state
    screenshot_path = "/sandbox/auto-allow-extension/test_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at {screenshot_path}")

    # Check if the button was clicked
    button = driver.find_element(By.CSS_SELECTOR, "article button")
    button_class = button.get_attribute("class")

    if "clicked" in button_class:
        print("Test Passed: Button was clicked by the extension.")
    else:
        print("Test Failed: Button was not clicked.")

except Exception as e:
    print(f"Test Failed with Exception: {e}")

finally:
    driver.quit()