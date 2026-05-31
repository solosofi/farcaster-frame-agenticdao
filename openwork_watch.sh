#!/bin/bash
# Production Openwork submission loop
# Reads API key from Wiki Layer, submits to highest-value open jobs every 2 minutes
while true; do
  python3 /home/user/farcaster-frame/openwork_loop.py >> /home/user/farcaster-frame/openwork_loop.log 2>&1
  sleep 120
done
