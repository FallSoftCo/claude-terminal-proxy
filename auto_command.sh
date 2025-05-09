#!/bin/bash

# This script watches for changes to the command file and executes them automatically
# Claude can write commands to the file, and they'll be executed automatically

COMMAND_FILE="/home/ai/Development/claude-terminal-proxy/next_command.txt"
TMUX_SESSION="claude"
TMUX_SOCKET="/tmp/claude-tmux-socket"
LAST_MODIFIED=0

echo "Starting automatic command execution..."
echo "Commands written to $COMMAND_FILE will be executed automatically"
echo "Press Ctrl+C to stop"

while true; do
  if [ -f "$COMMAND_FILE" ]; then
    CURRENT_MODIFIED=$(stat -c %Y "$COMMAND_FILE")
    
    if [ "$CURRENT_MODIFIED" -gt "$LAST_MODIFIED" ] && [ -s "$COMMAND_FILE" ]; then
      # File has been modified and is not empty
      COMMAND=$(cat "$COMMAND_FILE")
      
      # Only execute non-empty commands
      if [ ! -z "$COMMAND" ]; then
        echo "Executing: $COMMAND"
        
        # Send the command to tmux
        tmux -S "$TMUX_SOCKET" send-keys -t "$TMUX_SESSION" "$COMMAND" Enter
        
        # Clear the command file
        echo "" > "$COMMAND_FILE"
        
        echo "Command executed at $(date)"
      fi
      
      LAST_MODIFIED=$CURRENT_MODIFIED
    fi
  fi
  
  # Sleep to avoid high CPU usage
  sleep 1
done
