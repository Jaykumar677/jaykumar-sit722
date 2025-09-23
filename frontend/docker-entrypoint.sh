#!/bin/sh
# Replace env vars in the template and generate config.js
envsubst < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js
exec "$@"
