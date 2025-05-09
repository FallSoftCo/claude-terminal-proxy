#!/bin/bash

# Create a marker file to indicate free command mode is enabled
touch /home/ai/Development/claude-terminal-proxy/.free_command_mode

# Set permissions
chmod 644 /home/ai/Development/claude-terminal-proxy/.free_command_mode

echo "Free command mode ENABLED. Claude can now run terminal commands without confirmation."
echo "To disable this mode, run: rm /home/ai/Development/claude-terminal-proxy/.free_command_mode"