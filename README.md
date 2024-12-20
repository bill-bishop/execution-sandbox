# Sandboxed Environment with Flask API

This project creates a sandboxed environment with endpoints to execute commands and manage files.

## Project Structure

```
sandbox_project/
├── sandbox_server.py       # Flask server code
├── Dockerfile              # Docker image definition for the sandbox
├── requirements.txt        # Python dependencies
├── sandbox/                # Directory for sandbox files
└── README.md               # Instructions for running the project
```

## Setup Instructions

### 1. Build the Sandbox Docker Image

```bash
docker build -t sandbox .
```

### 2. Run the Flask Server

Install dependencies and start the Flask server:

```bash
pip install -r requirements.txt
python sandbox_server.py
```

### 3. Test the Endpoints

#### Execute a Command
```bash
curl -X POST http://localhost:8080/execute -H "Content-Type: application/json" -d '{"command": "ls"}'
```

#### Read a File
```bash
curl "http://localhost:8080/read?filename=test.txt"
```

#### Write a File
```bash
curl -X POST http://localhost:8080/write -H "Content-Type: application/json" -d '{"filename": "newfile.txt", "content": "Hello, Sandbox!"}'
```

### 4. Run the Sandbox Container

You can run the Docker container for additional isolation:

```bash
docker run --name sandbox -d --rm sandbox
```

## Security Notes

- Validate inputs to avoid path traversal attacks.
- Limit command execution and enforce resource constraints.
- Use non-root users to run the server and Docker container.
