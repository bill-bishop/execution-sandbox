# scrape_megamillions.py
# Updated script to scrape Mega Millions data with improved targeting and dynamic handling.

import requests
from bs4 import BeautifulSoup
import csv
import os

# URL of the Mega Millions historical data page
URL = "https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx"

# File path to save the CSV
OUTPUT_FILE = os.path.join("data", "mega_millions_data.csv")

def scrape_megamillions():
    """Scrape historical Mega Millions data and save it to a CSV file."""
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table based on its structure and attributes
    table = soup.find("table", {"class": "table-style-two"})
    if not table:
        print("Failed to locate the data table on the page. It may require JavaScript rendering.")
        return

    rows = table.find_all("tr")

    # Extract headers and data
    data = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        data.append([cell.get_text(strip=True) for cell in cells])

    # Write the data to a CSV file
    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    print(f"Data successfully saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_megamillions()