#!/bin/bash

# Kill any existing API server processes
pkill -f command_api_server.py

# Start the API server in the background
cd "$(dirname "$0")"
nohup python3 command_api_server.py > command_api_server.log 2>&1 &

echo "API server started with PID: $!"
echo "Server is running at http://localhost:3456"
echo "Check command_api_server.log for details"