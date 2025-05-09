#!/usr/bin/env python3
"""
Claude Free Command Client

A version of the terminal client that runs without requiring confirmation through Claude's UI.
This script is meant to be called by Claude's Task tool.
"""

import subprocess
import sys
import os
import argparse

def check_free_mode_enabled():
    """Check if free command mode is enabled."""
    marker_file = "/home/ai/Development/claude-terminal-proxy/.free_command_mode"
    return os.path.exists(marker_file)

def send_tmux_command(command, session_name="claude", socket_path="/tmp/claude-tmux-socket"):
    """Send a command to the tmux session."""
    try:
        subprocess.run(
            ["tmux", "-S", socket_path, "send-keys", "-t", session_name, command, "Enter"],
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Error: Failed to send command to tmux session {session_name}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Claude Free Command Client")
    parser.add_argument("command", help="The command to execute in the tmux session")
    
    args = parser.parse_args()
    
    if not check_free_mode_enabled():
        print("Error: Free command mode is not enabled.")
        print("Run ./enable_free_mode.sh to enable it.")
        sys.exit(1)
    
    # Send the command to tmux
    send_tmux_command(args.command)
    print(f"Command sent: {args.command}")

if __name__ == "__main__":
    main()