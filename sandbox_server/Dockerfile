# Use an official Python Alpine base image
FROM python:3.10-alpine

# Install Node.js and npm (if needed for other parts)
RUN apk add --no-cache nodejs npm

# Set up the working directory for server code
WORKDIR /app

# Copy project files into /app
COPY . /app/sandbox_server

# Expose API port
EXPOSE 8080

# Install Python dependencies
RUN pip install --no-cache-dir -r sandbox_server/requirements.txt

# Start the Flask server
CMD ["python", "-m", "sandbox_server.app"]