#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Install test dependencies
pip install pytest pytest-asyncio

# Run the tests
pytest --maxfail=1 --disable-warnings