# Sandboxed Environment with Flask API

This project creates a sandboxed environment with a Flask server running inside a Docker container. The server allows you to execute commands and interact with files in a controlled environment.

## Sandbox (with Flask interface) Setup Instructions

#### Build

Run the following command to build the sandbox server API Docker image:

```bash
docker build -t sandbox-server sandbox-server
```

Run the following command to build the Nginx router Docker image:

```bash
docker build -t terminal terminal
```

##### Ngrok

Make an account at http://ngrok.com and retrieve your authtoken.

Run an interactive root shell using the `wernight/ngrok` docker base image:

```bash
docker run -it --name temp-ngrok wernight/ngrok sh
```

Then update ngrok:

```bash
ngrok update
```

Then add your authtoken:

```bash
ngrok config add-authtoken <your-ngrok-auth-token>
```

Before `exit`ing the interactive shell, run this outside it to commit the now updated & authorized ngrok image:

```bash
docker commit temp-ngrok ngrok-auth
```

##### Run Containers Within Same Network

1. Create a shared network:
   ```bash
   docker network create sandbox-net
   ```
2. Start the python sandbox server in this network, and mount the ./sandbox volume (or any desired folder to use as the /sandbox mounted drive) to /sandbox 
   ```bash
   docker run --rm -d --network sandbox-net --name sandbox -v %CD%/sandbox:/sandbox sandbox-server:latest
   ```
4. Start the Nginx router in this network:
   ```bash
   docker run --rm -d --network sandbox-net --name sandbox-router terminal:latest
   ```
4. Start Ngrok in the same network (in interactive mode so you can get the random url):
   ```bash
   docker run --rm -it --network sandbox-net --name ngrok-auth ngrok-auth:latest ngrok http sandbox-router:80
   ```

