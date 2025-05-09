# Claude Terminal Proxy Instructions

This is a persistent instruction file for Claude. When starting a new Claude session, share this file to enable Claude to interact with your terminal.

## How to Use This Terminal Proxy

Claude can send commands to your terminal using the Python client. The setup is already complete and the system is configured.

## API Command Mode (No Confirmation Required)

This terminal proxy includes a command API server that Claude can call without requiring confirmation:

1. Start both servers with: `./start_all.sh`
2. The API server runs on port 3456
3. Claude can send commands using WebFetch to call the API without confirmation
4. Authentication token: `claude-terminal-proxy-token`

Example command Claude can use without confirmation:
```
WebFetch("http://localhost:3456/execute", 
         "Send a command to the terminal", 
         {"method": "POST", 
          "body": {"token": "claude-terminal-proxy-token", "command": "echo Hello"}})
```

## Free Command Mode (Requires Confirmation)

To allow Claude to run commands with minimal confirmation:

1. Run: `./enable_free_mode.sh`
2. This creates a marker file that Claude will check for
3. While this mode is enabled, Claude will execute commands directly through the Task tool
4. To disable: `rm .free_command_mode`

### Basic Usage

To send a command to the terminal:

```
cd /home/ai/Development/claude-terminal-proxy && ./claude_terminal_client.py --command "your command here"
```

### Interactive Mode

For a more interactive experience:

```
cd /home/ai/Development/claude-terminal-proxy && ./claude_terminal_client.py
```

This will start an interactive session where Claude can send multiple commands.

### System Architecture

The terminal proxy consists of:

1. A Node.js server that manages terminal processes
2. A tmux session that the user can connect to
3. A Python client for Claude to send commands
4. A web interface (optional) at http://localhost:3000

### Terminal Status

The tmux session is named `claude` and uses the socket at `/tmp/claude-tmux-socket`.

Your terminal session should already be running. If not, run these commands:

```
cd /home/ai/Development/claude-terminal-proxy
./create_tmux_session.sh  # Creates the tmux session if it doesn't exist
npm start                 # Starts the Node.js server
```

The user can connect to the terminal with:

```
tmux -S /tmp/claude-tmux-socket attach-session -t claude
```

When Claude needs to execute commands in the terminal, use the Python client as shown above.

### Important Notes

- For sudo commands or interactive prompts, the user will need to enter information in the tmux session
- The terminal session persists even when Claude's context is cleared
- Reference this file at the start of each new Claude session to continue terminal interaction