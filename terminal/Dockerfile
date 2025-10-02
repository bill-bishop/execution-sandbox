# Start with the official Nginx base image
FROM nginx:latest

# Copy custom Nginx configuration file
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy static files (optional)
COPY ./html /usr/share/nginx/html

#todo: auto copy dropcode client dist
#COPY ../dropcode-client/dist/dropcode-client/browser /usr/share/nginx/html

# Expose port 80 for the Nginx server
# EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
