# Execution Sandbox

This sandbox environment allows running isolated commands inside containers.

## Building the sandbox server

```bash
docker build -t sandbox_server sandbox_server
```

## Running the sandbox server

```bash
docker run --rm -d --network sandbox-net --name sandbox -v %CD%/sandbox:/sandbox sandbox_server:latest
```