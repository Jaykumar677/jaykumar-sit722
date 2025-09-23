#!/bin/sh

# Replace placeholders with environment variables and generate config.js
envsubst < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js

# Start nginx
exec nginx -g 'daemon off;'
