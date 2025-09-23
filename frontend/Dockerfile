# Use a lightweight web server
FROM nginx:alpine

# Install envsubst for variable substitution
RUN apk add --no-cache gettext

# Copy frontend files
COPY index.html /usr/share/nginx/html/
COPY main.js /usr/share/nginx/html/
COPY config.template.js /usr/share/nginx/html/config.template.js

# Add entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose port 80
EXPOSE 80

# Run entrypoint before starting nginx
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
