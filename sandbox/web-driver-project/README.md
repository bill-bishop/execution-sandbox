# Web Driver Project

A simple Python project to interact with web pages using Selenium WebDriver.

## Requirements
- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (or equivalent driver for your browser)

## Setup
1. **Install Selenium**:
   ```bash
   pip install selenium
   ```

2. **Download Browser Driver**:
   - For Google Chrome, download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).
   - Ensure the driver executable is in your PATH or specify its location in the script.

3. **Run the Script**:
   ```bash
   python src/web_driver_script.py
   ```

## Features
- Opens Google and performs a search for a given query.
- Prints the titles of the first 5 search results.

## Example Usage
- The script is pre-configured to search for "OpenAI ChatGPT".
- Modify the `search_google` function call in `web_driver_script.py` to use a different query.

## Notes
- Ensure the browser version matches the driver version.
- Add error handling and custom logic as needed for complex interactions.

---

### License
MIT