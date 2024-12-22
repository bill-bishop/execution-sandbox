# Use an official Python Alpine base image
FROM python:3.10-alpine

# Install necessary tools
RUN apk add --no-cache nodejs npm

# Set up the working directory
WORKDIR /sandbox

# Copy the sandbox-server into /sandbox/sandbox-server
COPY ./sandbox-server /sandbox/sandbox-server

# Install dependencies
WORKDIR /sandbox/sandbox-server
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Expose port 8080 for Flask
EXPOSE 8080

# Run the Flask server from /sandbox/sandbox-server
CMD ["python", "app.py"]