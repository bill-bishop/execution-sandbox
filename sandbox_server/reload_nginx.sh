#!/bin/sh
# Stub for nginx reload script
# In real deployment, this would reload nginx after updating upstreams

if nginx -t; then
  echo "Reloading nginx..."
  nginx -s reload
else
  echo "Nginx config test failed"
fi