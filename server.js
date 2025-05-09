const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const pty = require('node-pty');
const os = require('os');
const path = require('path');
const fs = require('fs');

// Create express app and HTTP server
const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Log startup information to help with reconnection
const startupLog = () => {
  const timestamp = new Date().toISOString();
  const logMessage = `
==========================================================
  CLAUDE TERMINAL PROXY SERVER
  Started: ${timestamp}
  
  To interact with this terminal in Claude:
  1. Share CLAUDE.md with Claude at the start of your session
  2. Use the Python client to send commands:
     ./claude_terminal_client.py --command "your command"
  
  Session info:
  - Tmux socket: /tmp/claude-tmux-socket
  - Tmux session: claude
  - Web interface: http://localhost:3000
==========================================================
`;
  console.log(logMessage);
  
  // Append to a log file for persistence
  fs.appendFileSync(
    path.join(__dirname, 'terminal-proxy.log'), 
    logMessage + "\n", 
    { encoding: 'utf8' }
  );
};

// Serve static files
app.use(express.static(path.join(__dirname, 'static')));

// Terminal process spawning
const terminals = {};
const logs = {};

io.on('connection', (socket) => {
  console.log('Client connected');
  
  // Create terminal
  socket.on('create', (cols, rows) => {
    const shell = process.platform === 'win32' ? 'powershell.exe' : 'bash';
    const env = Object.assign({}, process.env);
    env.TERM = 'xterm-256color';
    
    // Create terminal process
    const term = pty.spawn(shell, [], {
      name: 'xterm-color',
      cols: cols || 80,
      rows: rows || 24,
      cwd: process.cwd(),
      env: env
    });
    
    console.log(`Created terminal with PID: ${term.pid}`);
    terminals[term.pid] = term;
    logs[term.pid] = '';
    
    // Send terminal PID to client
    socket.emit('pid', term.pid);
    
    // Handle terminal data
    term.onData(data => {
      logs[term.pid] += data;
      socket.emit('data', data);
    });
    
    // Handle client data (commands)
    socket.on('data', (data) => {
      term.write(data);
    });
    
    // Handle terminal resize
    socket.on('resize', (cols, rows) => {
      term.resize(cols, rows);
    });
    
    // Handle disconnect
    socket.on('disconnect', () => {
      console.log(`Client disconnected from terminal ${term.pid}`);
      // Keep the terminal running for tmux to attach
    });
  });
});

// Start server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  startupLog();
});