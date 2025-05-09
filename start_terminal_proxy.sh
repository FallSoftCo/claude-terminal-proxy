#!/bin/bash

# Start terminal proxy server and create tmux session
cd "$(dirname "$0")"

echo "Ensuring tmux session exists..."
./create_tmux_session.sh

# Check if xterm files exist, download if needed
if [ ! -f ./static/js/xterm.js ]; then
  echo "xterm.js files not found. Downloading..."
  ./download_xterm.js
fi

# Start the server
echo "Starting terminal proxy server..."
npm start