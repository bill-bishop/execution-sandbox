# Stage 1: Build and Test
FROM python:3.10-slim as builder

WORKDIR /app

# Copy application files
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./requirements.txt /app/
COPY ./test.sh /app/

# Install application dependencies
RUN pip install -r requirements.txt

# Run tests
RUN ./test.sh

# Stage 2: Final Image
FROM python:3.10-slim

WORKDIR /app

# Copy application files from the build stage
COPY ./src /app/src
COPY ./requirements.txt /app/

# Install runtime dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8025

# Run the application
CMD ["python", "src/server.py"]