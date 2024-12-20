# Sandboxed Environment with Flask API

This project creates a sandboxed environment with a Flask server running inside a Docker container. The server allows you to execute commands and interact with files in a controlled environment.

## Project Structure

```
sandbox_project/
├── nginx/
│   ├── html/
│   │   ├── index.html
│   ├── nginx/
│   │   ├── Dockerfile
│   │   ├── nginx.conf
├── ngrok/
│   ├── Dockerfile
├── sandbox/
│   ├── test.txt
├── Dockerfile
├── README.md
├── requirements.txt
├── sandbox_server.py
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

curl -X POST [http://localhost:8080/execute](http://localhost:8080/execute) -H "Content-Type: application/json" -d "{"command": "ls"}"

#### Read a File

To read a file inside the sandbox, use:

curl "[http://localhost:8080/read?filename=test.txt](http://localhost:8080/read?filename=test.txt)"

#### Write a File

To write a file to the sandbox:

curl -X POST [http://localhost:8080/write](http://localhost:8080/write) -H "Content-Type: application/json" -d '{"filename": "newfile.txt", "content": "Hello, Sandbox!"}'

### Nginx Setup Instructions

#### 1. Build the Nginx Docker Image

Navigate to the `nginx` folder:

```bash
cd nginx
```

Run the following command to build the Nginx Docker image:

```bash
docker build -t my-nginx-server .
```

#### 2. Run the Nginx Server with Volume Mapping

Run the following command to start the Nginx container, mounting the `html` directory as a volume:

##### PowerShell Example

```bash
docker run --rm -d -p 8081:80 -v ${PWD}/html:/usr/share/nginx/html nginx
```

##### Command Prompt Example

```cmd
docker run --rm -d -p 8081:80 -v %CD%\html:/usr/share/nginx/html nginx
```

#### 3. Test the Nginx Server

- Visit: [http://localhost:8081](http://localhost:8081) to view the default page.
- Update or add files in the `html` directory while the container is running to see changes immediately.

### Ngrok Setup Instructions

#### Run Ngrok in Host Mode or Same-Network Container

To expose your server to the internet using Ngrok, you must either run the Ngrok container in host mode or route it to a container on the same Docker network as the server.

##### Host Mode Example

Run the Ngrok container in host mode to access a server running on the host machine:

```bash
docker run --rm --network host my-ngrok ngrok http localhost:8081
```

##### Same-Network Example

If the server is in a Docker container, ensure both Ngrok and the server are on the same Docker network:

1. Create a shared network:
   ```bash
   docker network create sandbox-net
   ```
2. Start the server in this network:
   ```bash
   docker run --rm --network sandbox-net --name sandbox-server -p 8081:80 my-nginx-server
   ```
3. Start Ngrok in the same network:
   ```bash
   docker run --rm --network sandbox-net my-ngrok ngrok http sandbox-server:80
   ```

## Notes

- All commands and file interactions occur inside the container's `/sandbox` directory.
- Ensure your Docker installation is properly set up and accessible.
- For Nginx, ensure the `html` folder contains an `index.html` or appropriate files to serve.

