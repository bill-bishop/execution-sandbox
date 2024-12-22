# Use an official Python Alpine base image
FROM python:3.10-alpine

# Install Node.js and npm
RUN apk add --no-cache nodejs npm

# Set up the working directory
WORKDIR /sandbox

# Copy project files and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask server port
EXPOSE 8080

# Start the Flask server
CMD ["python", "sandbox_server.py"]
