# Sandboxed Environment with Flask API

This project creates a sandboxed environment with a Flask server running inside a Docker container. The server allows you to execute commands and interact with files in a controlled environment.

## Project Structure

```
sandbox_project/
├── sandbox_server.py       # Flask server code
├── Dockerfile              # Dockerfile for container setup
├── requirements.txt        # Python dependencies
└── README.md               # Setup instructions
```

## Setup Instructions

### 1. Build the Docker Image

Run the following command to build the Docker image:

docker build -t sandbox .

### 2. Run the Docker Container

Use the following command to start the container and expose the server:

docker run -p 8080:8080 --rm sandbox

This command runs the container, exposing the Flask server on port 8080.

### 3. Test the Endpoints

#### Execute a Command

Use the following `curl` command to execute a command inside the container:

curl -X POST http://localhost:8080/execute -H "Content-Type: application/json" -d "{\"command\": \"ls\"}"

#### Read a File

To read a file inside the sandbox, use:

curl "http://localhost:8080/read?filename=test.txt"

#### Write a File

To write a file to the sandbox:

curl -X POST http://localhost:8080/write -H "Content-Type: application/json" -d '{"filename": "newfile.txt", "content": "Hello, Sandbox!"}'

## Notes

- All commands and file interactions occur inside the container's `/sandbox` directory.
- Ensure your Docker installation is properly set up and accessible. 
