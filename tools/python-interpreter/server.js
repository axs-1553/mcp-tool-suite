// Python Interpreter Server
// A simple TCP server that executes Python code and returns the output

import { spawn } from 'child_process';
import { createServer } from 'net';

const PYTHON_PATH = 'python'; // User can configure their Python path
const DEFAULT_PORT = 3000; // User can configure their preferred port

const server = createServer((socket) => {
  let dataBuffer = '';
  let pythonProcess = null;

  socket.on('data', (data) => {
    dataBuffer += data.toString();
    
    try {
      const message = JSON.parse(dataBuffer);
      dataBuffer = '';
      
      if (message.type === 'execute') {
        if (pythonProcess) {
          pythonProcess.kill();
        }

        pythonProcess = spawn(PYTHON_PATH, ['-c', message.code]);
        let output = '';
        let error = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          error += data.toString();
        });

        pythonProcess.on('close', (code) => {
          socket.write(JSON.stringify({
            status: code === 0 ? 'success' : 'error',
            output: output,
            error: error
          }) + '\n');
        });
      }
    } catch (err) {
      if (err instanceof SyntaxError) {
        // Incomplete JSON, wait for more data
        return;
      }
      socket.write(JSON.stringify({
        status: 'error',
        error: err.message
      }) + '\n');
    }
  });

  socket.on('error', (err) => {
    console.error('Socket error:', err);
  });
});

server.listen(DEFAULT_PORT, () => {
  console.log(`Python interpreter server running on port ${DEFAULT_PORT}`);
});

// Handle server shutdown
process.on('SIGINT', () => {
  server.close(() => {
    console.log('Server shutdown complete');
    process.exit(0);
  });
});