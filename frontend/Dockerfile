# Use a lightweight web server
FROM nginx:alpine

# Copy all frontend files into nginx's html directory
COPY . /usr/share/nginx/html

# Expose port 80 for web traffic
EXPOSE 80

# Start nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]
