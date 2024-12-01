# Python Interpreter MCP Tool

Execute Python code in virtual environments through Model Context Protocol.

## Prerequisites
- Node.js v18.x or later
- npm or yarn
- Python 3.x

## Installation
```bash
# Install MCP SDK dependencies
npm install @modelcontextprotocol/sdk

# Set up virtual environment directory
mkdir .venvs
python -m venv .venvs/default
```

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

## Running the Server
```bash
# Make server executable
chmod +x server.js

# Run directly
./server.js

# Or via node
node server.js
```

## Virtual Environments
- Default environment in `.venvs/default`
- Create additional environments in `.venvs/` directory
- Specify environment name with `venv` parameter in requests