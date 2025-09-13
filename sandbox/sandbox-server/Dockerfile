# Use an official Python Alpine base image
FROM python:3.10-alpine

# Install Node.js and npm
RUN apk add --no-cache nodejs npm

# Set up the working directory
WORKDIR /sandbox/sandbox-server

# Copy project files and install dependencies
# todo: fix root-build nonsense, use docker compose or something
COPY . /sandbox/sandbox-server

# todo: fix this pathing ****ery - this server has been being built from one level above & therefore executing /sandbox/sandbox_server.py instead of sandbox_server.py (the one in this directory)
# for now ... I'll build from above, copy the ./sandbox-server/sandbox_server.py file into ./sandbox/ and continue as is, ensuring this file is building the server code from ./sandbox-server/ 
# then, once BAU is restored, i'll fix this baloney

RUN pip install --no-cache-dir -r requirements.txt

# Start the Flask server
CMD ["python", "app.py"]
