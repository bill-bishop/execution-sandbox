FROM wernight/ngrok

# Copy the ngrok configuration file into the default location
COPY ngrok.yml /.ngrok2/ngrok.yml

#  chmod 644 /.ngrok2/ngrok.yml

# Run ngrok with the http command
CMD ["ngrok", "--config", "/.ngrok2/ngrok.yml", "http", "sandbox-router:80"]