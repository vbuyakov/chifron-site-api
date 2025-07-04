#!/bin/sh
set -e

# Replace environment variables in all .template files
for template in /etc/nginx/templates/*.template; do
  # Skip if the glob didn't match any files
  [ -e "$template" ] || continue
  
  # Remove .template extension for the output file
  output_file="/etc/nginx/conf.d/$(basename "$template" .template)"
  
  # Use envsubst to replace environment variables
  envsubst '${NGINX_HOST} ${SERVER_PORT}' < "$template" > "$output_file"
  
  echo "Generated $output_file from $(basename "$template")"
done

# Test the configuration
nginx -t

# Start Nginx
nginx -g 'daemon off;'
