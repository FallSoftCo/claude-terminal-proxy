const pty = require('node-pty');
const readline = require('readline');

// Function to execute commands in tmux
function executeTmuxCommand(command) {
  return new Promise((resolve, reject) => {
    const term = pty.spawn('tmux', ['-S', '/tmp/claude-tmux-socket', 'send-keys', '-t', 'claude', command, 'Enter']);
    
    let output = '';
    term.onData(data => {
      output += data;
    });
    
    term.onExit(({ exitCode }) => {
      if (exitCode === 0) {
        resolve(output);
      } else {
        reject(new Error(`Command failed with exit code ${exitCode}`));
      }
    });
  });
}

// CLI interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('Claude Terminal Command Interface');
console.log('Type commands to send to the tmux session, or "exit" to quit');

function promptCommand() {
  rl.question('Claude> ', async (command) => {
    if (command.toLowerCase() === 'exit') {
      rl.close();
      return;
    }
    
    try {
      await executeTmuxCommand(command);
      console.log('Command sent successfully');
    } catch (error) {
      console.error('Error sending command:', error.message);
    }
    
    promptCommand();
  });
}

promptCommand();