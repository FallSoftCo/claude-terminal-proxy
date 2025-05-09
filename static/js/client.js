document.addEventListener('DOMContentLoaded', () => {
    // Connect to socket.io server
    const socket = io();

    // Create terminal
    const terminal = new Terminal({
        cursorBlink: true,
        macOptionIsMeta: true,
        scrollback: 1000,
        theme: {
            background: '#1e1e1e',
            foreground: '#f0f0f0'
        }
    });

    // Load FitAddon
    const fitAddon = new FitAddon.FitAddon();
    terminal.loadAddon(fitAddon);

    // Open terminal
    terminal.open(document.getElementById('terminal-container'));
    fitAddon.fit();

    // Handle socket connection
    socket.on('connect', () => {
        // Create terminal with current size
        const dimensions = fitAddon.proposeDimensions();
        socket.emit('create', dimensions.cols, dimensions.rows);
    });

    // Handle terminal data
    socket.on('data', (data) => {
        terminal.write(data);
    });

    // Handle PID
    socket.on('pid', (pid) => {
        document.getElementById('terminal-id').textContent = pid;
        
        // Initialize tmux
        socket.emit('data', `tmux -S /tmp/claude-tmux-socket new-session -A -s claude\r`);
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        fitAddon.fit();
        const dimensions = fitAddon.proposeDimensions();
        socket.emit('resize', dimensions.cols, dimensions.rows);
    });

    // Handle user input
    terminal.onData(data => {
        socket.emit('data', data);
    });
});