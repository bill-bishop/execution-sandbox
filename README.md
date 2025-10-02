# Sandboxed Environment with Flask API

This project creates a sandboxed environment with a Flask server running inside a Docker container. The server allows you to execute commands and interact with files in a controlled environment.

## Sandbox (with Flask interface) Setup Instructions

#### Build

Run the following command to build the latest sandbox server API Docker image:

```bash
docker build -t sandbox_server sandbox_server
docker build -t sandbox_server:nightly sandbox_server # nightly
```

Run the following command to build the Nginx router Docker image:

```bash
docker build -t terminal terminal
docker build -t terminal:nightly terminal # nightly
```


##### Run Containers Within Same Network

1. Create a shared network:
   ```bash
   docker network create sandbox-net
   ```
2. Start the python sandbox server in this network, and mount any desired folder to /sandbox (below example mounts this project root):
   ```bash
   docker run --rm -d --network sandbox-net --name sandbox -v %CD%/../../:/sandbox --env-file .env sandbox_server:latest
   docker run --rm -d --network sandbox-net --name sandbox -v %CD%/../../:/sandbox --env-file .env sandbox_server:nightly # nightly
   ```
3. Start the Nginx router in this network, exposing port 80:
   ```bash
   docker run --rm -d --network sandbox-net --name sandbox-router -p 80:80 terminal:latest
   docker run --rm -d --network sandbox-net --name sandbox-router -p 80:80 terminal:nightly # nightly
   ```

##### Testing Nightly Version

Build the nightly sandbox_server image, kill the sandbox, wait, start the nightly container:

```bash
docker build -t sandbox_server:nightly sandbox_server && docker kill sandbox && sleep 3 && docker run --rm -d --network sandbox-net --name sandbox -v %CD%/../../:/sandbox --env-file .env sandbox_server:nightly
```

Same for the nginx router & UI assets:

```bash
cd ../dropcode-client && npm run build && cd ../execution-sandbox && docker build -t terminal:nightly terminal && docker kill sandbox-router && sleep 3 && docker run --rm -d --network sandbox-net --name sandbox-router -p 80:80 terminal:nightly
```

##### Cloudflare Tunnel Setup

Expose your local Nginx server via a Cloudflare Tunnel. Make sure you have a Cloudflare account and a domain managed by Cloudflare.

1. Install `cloudflared` and log in:
   ```powershell
   cloudflared login
   ```
   This will open a browser window to authenticate with Cloudflare and save your credentials locally.

2. Create a new tunnel:
   ```powershell
   cloudflared tunnel create dropcode-tunnel
   ```
   This will generate a credentials JSON file in your `.cloudflared` directory. Keep this file secret.

3. Route the tunnel to your domain:
   ```powershell
   cloudflared tunnel route dns dropcode-tunnel <your-domain>
   ```
   If the DNS record already exists, you may need to delete or update it manually in the Cloudflare dashboard.

4. Create a `config.yml` file in your `.cloudflared` directory:
   ```yaml
   tunnel: dropcode-tunnel

   ingress:
     - hostname: <your-domain>
       service: http://sandbox-router:80
     - service: http_status:404
   ```

5. Run the tunnel:
   ```powershell
   cloudflared tunnel run dropcode-tunnel
   ```


Now your sandbox is accessible through your public domain secured by Cloudflare Tunnel.