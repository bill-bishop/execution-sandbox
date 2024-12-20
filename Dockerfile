FROM ubuntu:latest

# Install basic tools
RUN apt-get update && apt-get install -y bash

# Create a working directory
WORKDIR /sandbox

# Restrict permissions
RUN chmod 700 /sandbox

CMD ["bash"]
