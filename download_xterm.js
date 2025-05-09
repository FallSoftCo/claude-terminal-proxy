#!/bin/bash

# Create directories if they don't exist
mkdir -p static/js
mkdir -p static/css

# Download xterm.js
curl -L https://unpkg.com/xterm@5.3.0/lib/xterm.js -o static/js/xterm.js
curl -L https://unpkg.com/xterm@5.3.0/css/xterm.css -o static/css/xterm.css

# Download xterm-addon-fit
curl -L https://unpkg.com/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js -o static/js/xterm-addon-fit.js

echo "Downloaded xterm.js and addon-fit successfully!"