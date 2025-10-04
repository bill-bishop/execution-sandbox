# Use an official Python Alpine base image
FROM python:3.10-alpine

# Install Node.js, npm, Chromium, Git
RUN apk add --no-cache nodejs npm chromium git \
    && git config --global user.name "HermesAI" \
    && git config --global user.email "agent@hermesai.dev"

# Set up the working directory for server code
WORKDIR /app

# Copy project files into /app
COPY . /app/sandbox_server

# Expose API port
EXPOSE 8080

# turn off angular analytics
ENV NG_CLI_ANALYTICS=false
ENV CHROME_BIN=/usr/bin/chromium

# Install Python dependencies
RUN pip install --no-cache-dir -r sandbox_server/requirements.txt

# Start the Flask server
CMD ["python", "-m", "sandbox_server.app"]