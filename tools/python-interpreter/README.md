# Python Interpreter Server

A Node.js TCP server that executes Python code and returns the output.

## Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "python-interpreter": {
    "command": "node",
    "args": ["path/to/python-interpreter-server.js"],
    "type": "module"
  }
}
```

## Usage

The server accepts JSON messages with:
- `type`: "execute"
- `code`: Python code to run

Returns JSON response with:
- `status`: "success" or "error" 
- `output`: stdout content
- `error`: stderr content if any