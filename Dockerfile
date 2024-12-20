FROM python:3.10-slim

# Set up the working directory
WORKDIR /sandbox

# Copy project files and install dependencies
COPY . .
RUN pip install -r requirements.txt

# Expose Flask server port
EXPOSE 8080

# Start the Flask server
CMD ["python", "sandbox_server.py"]
