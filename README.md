# Claude Terminal Proxy

A simple terminal proxy that allows Claude Code to command a terminal session via tmux.

## Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Download xterm.js files:
   ```
   ./download_xterm.js
   ```

3. Start the server:
   ```
   npm start
   ```

4. Open the web interface at http://localhost:3000

## Connecting via tmux

There are two ways to create and connect to the tmux session:

1. **Create the session manually first (recommended):**
   ```
   ./create_tmux_session.sh
   tmux -S /tmp/claude-tmux-socket attach-session -t claude
   ```

2. **Wait for the web interface to create it:**
   Start the server with `npm start` and open the web interface first, which will create the tmux session automatically. Then connect with:
   ```
   tmux -S /tmp/claude-tmux-socket attach-session -t claude
   ```

Either approach will connect to the same session that's visible in the web interface.

## Sending Commands from Claude

Claude can send commands to the terminal using the `claude_command.js` script:

```
node claude_command.js
```

This provides a simple CLI where Claude can type commands that will be sent to the tmux session.

## Architecture

This system consists of:

1. A Node.js server with Socket.IO that creates and manages the terminal process
2. A web interface showing the terminal output
3. A tmux session that can be attached to from the client's terminal
4. A Claude command interface for sending commands to the tmux session

The web interface will automatically create a tmux session when started, making it easy to connect from your local terminal.
## Auto-Command System

For completely automated command execution without confirmation:

1. Start the auto-command monitor:
   ```
   ./auto_command.sh &
   ```

2. Claude will write commands to `next_command.txt`

3. Commands are automatically executed in the tmux session

4. This eliminates the need for confirmation on each command

5. To stop the auto-command system:
   ```
   pkill -f auto_command.sh
   ```

This provides the most seamless experience for terminal interaction between Claude and the user.
