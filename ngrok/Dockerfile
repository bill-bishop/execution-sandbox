FROM wernight/ngrok

# Set the ngrok auth token during build
ARG NGROK_AUTHTOKEN
RUN ngrok config add-authtoken $NGROK_AUTHTOKEN
