from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_google(query):
    """
    Opens a browser, navigates to Google, and searches for the provided query.

    Args:
        query (str): The search term to query on Google.
    """
    # Set up the WebDriver (ensure you have the correct driver installed for your browser)
    driver = webdriver.Chrome()  # Change to Firefox or another browser if needed

    try:
        # Open Google
        driver.get("https://www.google.com")

        # Find the search bar and enter the query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait to allow results to load
        time.sleep(3)

        # Print titles of the search results
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        print("Search Results:")
        for result in results[:5]:  # Limit to first 5 results
            print(result.text)

    finally:
        # Close the browser
        driver.quit()

# Example usage
if __name__ == "__main__":
    search_google("OpenAI ChatGPT")