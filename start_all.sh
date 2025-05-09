#!/bin/bash

# Start terminal proxy server and command API server
cd "$(dirname "$0")"

echo "Ensuring tmux session exists..."
./create_tmux_session.sh

# Check if xterm files exist, download if needed
if [ ! -f ./static/js/xterm.js ]; then
  echo "xterm.js files not found. Downloading..."
  ./download_xterm.js
fi

# Start the command API server in the background
echo "Starting command API server..."
./command_api_server.py > command_api_server.log 2>&1 &
API_PID=$!
echo "Command API server started with PID: $API_PID"

# Start the main terminal proxy server
echo "Starting terminal proxy server..."
npm start