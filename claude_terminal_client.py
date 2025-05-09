#!/usr/bin/env python3
"""
Claude Terminal Client

A client for Claude to send commands to a tmux session and receive output.
"""

import subprocess
import time
import argparse
import os
import sys
import re

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

def get_tmux_output(session_name="claude", socket_path="/tmp/claude-tmux-socket"):
    """Capture the current output from the tmux pane."""
    try:
        result = subprocess.run(
            ["tmux", "-S", socket_path, "capture-pane", "-p", "-t", session_name],
            check=True, capture_output=True, text=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        print(f"Error: Failed to capture output from tmux session {session_name}")
        return ""

def clear_tmux_screen(session_name="claude", socket_path="/tmp/claude-tmux-socket"):
    """Clear the tmux screen."""
    try:
        subprocess.run(
            ["tmux", "-S", socket_path, "send-keys", "-t", session_name, "clear", "Enter"],
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Error: Failed to clear tmux screen for session {session_name}")
        return False

def ensure_tmux_session(session_name="claude", socket_path="/tmp/claude-tmux-socket"):
    """Ensure the tmux session exists, creating it if necessary."""
    try:
        # Check if session exists
        result = subprocess.run(
            ["tmux", "-S", socket_path, "has-session", "-t", session_name],
            capture_output=True
        )
        
        if result.returncode != 0:
            # Create session
            subprocess.run(
                ["tmux", "-S", socket_path, "new-session", "-d", "-s", session_name],
                check=True
            )
            print(f"Created new tmux session: {session_name}")
        else:
            print(f"Connected to existing tmux session: {session_name}")
            
        # Set appropriate permissions
        os.chmod(socket_path, 0o777)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting up tmux session: {e}")
        return False

def interactive_mode():
    """Run in interactive mode, allowing Claude to send commands and see output."""
    ensure_tmux_session()
    
    print("Claude Terminal Client - Interactive Mode")
    print("Type commands to send to the tmux session")
    print("Use .clear to clear the terminal")
    print("Use .exit to quit")
    
    while True:
        try:
            command = input("Claude> ").strip()
            
            if command == ".exit":
                break
            elif command == ".clear":
                clear_tmux_screen()
                continue
            elif command.startswith(".wait"):
                # Format: .wait 2 (wait 2 seconds)
                parts = command.split()
                if len(parts) > 1 and parts[1].isdigit():
                    wait_time = int(parts[1])
                else:
                    wait_time = 1
                time.sleep(wait_time)
                continue
            elif command == ".output":
                output = get_tmux_output()
                print("\n--- BEGIN TERMINAL OUTPUT ---")
                print(output)
                print("--- END TERMINAL OUTPUT ---\n")
                continue
                
            # Send the command
            if command:
                send_tmux_command(command)
                # Wait a moment for command to execute
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break

def main():
    parser = argparse.ArgumentParser(description="Claude Terminal Client")
    parser.add_argument("--session", default="claude", help="Tmux session name")
    parser.add_argument("--socket", default="/tmp/claude-tmux-socket", help="Tmux socket path")
    parser.add_argument("--command", help="Single command to execute (non-interactive mode)")
    
    args = parser.parse_args()
    
    if args.command:
        # Non-interactive mode: run a single command
        ensure_tmux_session(args.session, args.socket)
        send_tmux_command(args.command, args.session, args.socket)
        time.sleep(0.5)  # Wait for command to execute
        print(get_tmux_output(args.session, args.socket))
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()