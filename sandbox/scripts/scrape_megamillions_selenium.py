# scrape_megamillions_selenium.py
# This script uses Selenium to scrape Mega Millions data dynamically.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import os

# File path to save the CSV
OUTPUT_FILE = os.path.join("data", "mega_millions_data.csv")

# URL of the Mega Millions historical data page
URL = "https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx"

def scrape_megamillions():
    """Scrape historical Mega Millions data using Selenium and save it to a CSV file."""
    # Initialize the Selenium WebDriver
    service = Service("/path/to/chromedriver")  # Update this with the path to your WebDriver
    driver = webdriver.Chrome(service=service)

    try:
        # Open the Mega Millions website
        driver.get(URL)

        # Wait for the table to load
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-style-two")))

        # Extract rows from the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Collect data from rows
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            data.append([cell.text.strip() for cell in cells])

        # Write the data to a CSV file
        with open(OUTPUT_FILE, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

        print(f"Data successfully saved to {OUTPUT_FILE}")

    except TimeoutException:
        print("Failed to load the table within the timeout period.")

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    scrape_megamillions()