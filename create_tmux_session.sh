#!/bin/bash

# Create tmux session if it doesn't exist
tmux -S /tmp/claude-tmux-socket has-session -t claude 2>/dev/null
if [ $? -ne 0 ]; then
  tmux -S /tmp/claude-tmux-socket new-session -d -s claude
  echo "Created new tmux session: claude"
else
  echo "Session 'claude' already exists"
fi

# Set socket permissions
chmod 777 /tmp/claude-tmux-socket
echo "Set permissions on socket: /tmp/claude-tmux-socket"

echo "You can now connect with: tmux -S /tmp/claude-tmux-socket attach-session -t claude"