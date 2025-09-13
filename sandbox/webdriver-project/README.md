# Selenium WebDriver Project

This project contains scripts and utilities for testing browser-based extensions and web interactions using Selenium WebDriver.

## Features
- Automated testing of browser extensions
- Headless and non-headless testing modes
- Modular test case management

## Project Structure
```
webdriver-project/
├── tests/                 # Test cases
├── drivers/               # WebDriver executables (if necessary)
├── screenshots/           # Screenshots for debugging
└── README.md              # Project documentation
```

## Installation
1. Install Python dependencies:
   ```bash
   pip install selenium
   ```
2. Ensure you have Chrome/Chromium and Chromedriver installed.

## Running Tests
To execute a test script, run:
```bash
python3 tests/<test_script>.py
```