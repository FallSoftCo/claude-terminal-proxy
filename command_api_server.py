#!/usr/bin/env python3
"""
Command API Server

A simple HTTP server that accepts commands and executes them in the tmux session.
Claude can use WebFetch to call this API without requiring confirmation.
"""

import http.server
import socketserver
import subprocess
import json
import urllib.parse
import os
from pathlib import Path

# Configuration
PORT = 3456
TMUX_SESSION = "claude"
TMUX_SOCKET = "/tmp/claude-tmux-socket"
AUTH_TOKEN = "claude-terminal-proxy-token"  # Simple authentication
LOG_FILE = Path(__file__).parent / "command_api.log"

class CommandHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Override to log to our file instead of stderr"""
        with open(LOG_FILE, 'a') as f:
            f.write(f"{self.log_date_time_string()} - {format % args}\n")
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse URL and query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Basic routing
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Command API Server Running")
        elif parsed_path.path == "/ping":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"pong")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def do_POST(self):
        """Handle POST requests for command execution"""
        if self.path == "/execute":
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                # Validate auth token
                if data.get('token') != AUTH_TOKEN:
                    self.send_response(401)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid token"}).encode())
                    return
                
                # Execute command
                if 'command' in data:
                    command = data['command']
                    success = self.execute_command(command)
                    
                    if success:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "success", "command": command}).encode())
                    else:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "error", "message": "Failed to execute command"}).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing command"}).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def execute_command(self, command):
        """Execute a command in the tmux session"""
        try:
            # Log the command
            with open(LOG_FILE, 'a') as f:
                f.write(f"{self.log_date_time_string()} - Executing command: {command}\n")
            
            # Send the command to tmux
            subprocess.run(
                ["tmux", "-S", TMUX_SOCKET, "send-keys", "-t", TMUX_SESSION, command, "Enter"],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            # Log the error
            with open(LOG_FILE, 'a') as f:
                f.write(f"{self.log_date_time_string()} - Error executing command: {e}\n")
            return False

def main():
    # Initialize log file
    with open(LOG_FILE, 'a') as f:
        f.write(f"=== Command API Server started on port {PORT} ===\n")
    
    # Create and start the HTTP server
    with socketserver.TCPServer(("", PORT), CommandHandler) as httpd:
        print(f"Command API Server running on port {PORT}")
        print(f"Use this URL in Claude: http://localhost:{PORT}/execute")
        print(f"Authentication token: {AUTH_TOKEN}")
        print(f"Log file: {LOG_FILE}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()