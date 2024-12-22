# Sandboxed Environment with Flask API

This project creates a sandboxed environment with a Flask server running inside a Docker container. The server allows you to execute commands and interact with files in a controlled environment.

## Sandbox (with Flask interface) Setup Instructions

#### Build

Run the following command to build the Docker image:

```bash
docker build -t sandbox-server sandbox-server
```

### 3. Test the Sandbox interface

#### Execute a Command

Use the following `curl` command to execute a command inside the container:

curl -X POST http://localhost:8080/execute -H "Content-Type: application/json" -d "{\"command\": \"ls\"}"

#### Read a File

To read a file inside the sandbox, use:

curl http://localhost:8080/read?filename=test.txt


#### 3. Test the Nginx Server

- Visit: [http://localhost:8081](http://localhost:8081) to view the default page.
- Update or add files in the `html` directory while the container is running to see changes immediately.

#### Write a File

To write a file to the sandbox:

curl -X POST http://localhost:8080/write -H "Content-Type: application/json" -d '{"filename": "newfile.txt", "content": "Hello, Sandbox!"}'

### Terminal UI + Nginx Router Setup Instructions

#### Build
Run the following command to build the Nginx Docker image:

```bash
docker build -t terminal terminal
```


### Ngrok Setup Instructions

#### Build

Your ngrok container must have a `/home/ngrok/.ngrok2/ngrok.yml` file with your ngrok authtoken, or you must run `add-authtoken` in the container.

You can use a temporary container to create a base image `ngrok-auth:latest` with your auth token:

```bash
docker run --name temp-ngrok wernight/ngrok ngrok config add-authtoken <your-ngrok-auth-token>
docker commit temp-ngrok ngrok-auth
docker rm temp-ngrok
```

##### Run Containers Within Same Network

1. Create a shared network:
   ```bash
   docker network create sandbox-net
   ```
2. Start the python sandbox server in this network, and mount the ./sandbox volume to /sandbox 
   ```bash
   docker run --rm -d --network sandbox-net --name sandbox-server -v %CD%/sandbox:/sandbox sandbox-server:latest
   ```
4. Start the Nginx router in this network:
   ```bash
   docker run --rm -d --network sandbox-net --name terminal terminal:latest
   ```
4. Start Ngrok in the same network (in interactive mode so you can get the random url):
   ```bash
   docker run --rm -it --network sandbox-net --name ngrok-auth ngrok-auth:latest ngrok http sandbox-router:80
   ```

## Notes

- All commands and file interactions occur inside the container's `/sandbox` directory.
- Ensure your Docker installation is properly set up and accessible.
- For Nginx, ensure the `html` folder contains an `index.html` or appropriate files to serve.

