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

Run the following command to build the PostreSQL Docker image:

```bash
docker build -t hermesdb database
docker build -t hermesdb:nightly database # nightly
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
   
#####

Rollback

```bash
docker run --rm -d --network sandbox-net --name sandbox -v %CD%/../../:/sandbox --env-file .env hermesai-backend:rollback
docker run --rm -d --network sandbox-net --name sandbox-router -p 80:80 hermesai-router:rollback
cloudflared tunnel run hermesai

```

##### Testing Nightly Version

Build the nightly sandbox_server image, kill the sandbox, wait, start the nightly container:

```bash
docker build -t sandbox_server:nightly sandbox_server && docker kill sandbox && sleep 3 && docker run --rm -d --network sandbox-net --name sandbox -v %CD%/../../:/sandbox --env-file .env sandbox_server:nightly
```

Same for the nginx router & UI assets:

```bash
cd ../dropcode-client && npm run build && cd ../../ && cp -R assets apps/execution-sandbox/terminal/html/ && cp apps/execution-sandbox/terminal/html/assets/favicon.ico apps/execution-sandbox/terminal/html/ && cd apps/execution-sandbox && docker build -t terminal:nightly terminal && docker kill sandbox-router && sleep 3 && docker run --rm -d --network sandbox-net --name sandbox-router -p 80:80 terminal:nightly
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
   cloudflared tunnel create hermesai
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
   cloudflared tunnel run hermesai
   ```


Now your sandbox is accessible through your public domain secured by Cloudflare Tunnel.



##### New steps:

from monorepo root: `docker compose build` and `docker compose up` -> view http://localhost:80

##### Digital Ocean: Docker Droplet Deployment

File sync to Docker Droplet: (temp til we have image repo based deployments):

from the parent folder above the monorepo:
```bash
wsl -d Ubuntu 
rsync -vhra ./dropcode-monorepo root@DROPLET_IP:/app --include='**.gitignore' --exclude='/.git' --filter=':- .gitignore'
```

This command tries to respect gitignore to avoid massive sync of unneeded files 
before rsync you must generate an ssh key and ensure the public key is in your droplet server's authorized_clients 

after this you can ssh into your droplet and `docker compose up` from the project dir 

local db backup

```bash
wsl -d Ubuntu 
rsync -vhra root@DROPLET_IP:/app/dropcode-monorepo/apps/execution-sandbox/sandbox_server/sandbox.db ./sandbox.backup.db
```
