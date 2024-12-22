# Custom Email Server

A simple custom email server for receiving and sending emails using Python and `aiosmtpd`.

---

## Features
- Receives emails for any address within the configured domain.
- Logs and saves received emails to a local file.
- Includes functionality to send emails.
- Fully tested using `pytest`.

---

## Requirements
- Docker installed on your system.

---

## Setup and Usage

### 1. Build the Docker Image
Run the following command to build the Docker image:
```bash
docker build -t email-server .
```

### 2. Run the Email Server
Run the container with:
```bash
docker run -p 8025:8025 -v $(pwd)/emails:/sandbox/email-server/emails email-server
```

- This command maps the `emails/` directory on your host machine to the `emails/` directory in the container.
- All received emails will be saved to the `emails/received_email.txt` file on your host machine.

### 3. Test the Server
You can manually send emails to the server using tools like `telnet` or an email client:
```bash
telnet localhost 8025
```
Or you can run the automated tests:
```bash
pytest
```

---

## Directory Structure
```
email-server/
├── Dockerfile
├── README.md
├── emails/      # Directory to store received emails
├── src/         # Source code for the server and email functionality
├── tests/       # Unit tests
├── test.sh      # Test runner script
├── requirements.txt
└── MANIFEST.in
```

---

## Notes
- Make sure port `8025` is available on your host machine.
- Adjust the `smtp_server` and credentials in the `send_email` function for sending emails via a real SMTP server.

---

## License
MIT