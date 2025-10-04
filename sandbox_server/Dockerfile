# Use an official Python Alpine base image
FROM python:3.10-alpine

# Install system dependencies (PostgreSQL client libs, Node.js, npm, Chromium, Git)
RUN apk add --no-cache \
    nodejs npm chromium git postgresql-dev gcc musl-dev python3-dev \
    && git config --global user.name "HermesAI" \
    && git config --global user.email "agent@hermesai.dev"

# Set up the working directory
WORKDIR /app

# Copy server source code
COPY . /app/sandbox_server

# Environment setup
ENV NG_CLI_ANALYTICS=false
ENV CHROME_BIN=/usr/bin/chromium
ENV FLASK_APP=sandbox_server
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/dropcode

# Install Python dependencies
RUN pip install --no-cache-dir -r sandbox_server/requirements.txt

# Initialize database migrations (safe to run even if directory exists)
RUN flask db init || true
RUN flask db migrate -m "initial schema" || true
RUN flask db upgrade || true

# Expose the API port
EXPOSE 8080

# Default command: run Flask app
CMD ["flask", "run"]