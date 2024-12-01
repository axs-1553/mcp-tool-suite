# Swiss Army Knife MCP Tool

A versatile tool for running Python scripts through the Model Context Protocol.

## Prerequisites
- Node.js v18.x or later
- npm or yarn
- Python 3.x

## Installation

1. Install MCP SDK and dependencies:
```bash
npm install @modelcontextprotocol/sdk
```

2. Set up the scripts directory:
```bash
mkdir scripts
```

3. Point MCP_HOME to your Node.js modules directory:
```bash
# Windows (PowerShell)
$env:MCP_HOME = "C:\Users\YourUsername\AppData\Roaming\npm\node_modules"

# Linux/Mac
export MCP_HOME="/usr/local/lib/node_modules"
```

## Configuration

Add to your `claude_desktop_config.json`:
```json
{
  "swiss-army-knife": {
    "command": "node",
    "args": ["path/to/swiss-army-knife/server.js"],
    "type": "module"
  }
}
```

## Running the Server

```bash
# Make server executable
chmod +x server.js

# Run the server
./server.js
```

## Creating Custom Scripts

1. Create a new Python script with `.sak.py` extension in the `scripts` directory
2. Follow this template:
```python
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show script information')
    # Add your custom arguments here
    args = parser.parse_args()

    if args.info:
        print("""
        Tool Name: Your Tool Name
        Description: What this tool does
        Usage: swiss-army-knife your-script-name --arg1 value1
        Arguments:
          --arg1: Description of argument 1
          --arg2: Description of argument 2
        Example:
          swiss-army-knife your-script-name --arg1 hello --arg2 world
        """)
        return

    # Your tool logic here

if __name__ == '__main__':
    main()
```

## Available Commands

- `--help`: Show script creation guide
- `--list`: Show all available scripts
- `--info <script_name>`: Show script documentation
- `<script_name> [args]`: Run a specific script

## Troubleshooting

1. Script not found:
   - Ensure script is in the `scripts` directory
   - Check file extension is `.sak.py`
   - Verify file permissions

2. Python errors:
   - Check Python installation: `python --version`
   - Verify script syntax
   - Check required packages are installed

3. Server connection issues:
   - Verify Claude Desktop is running
   - Check MCP_HOME environment variable
   - Ensure server path in config is correct

## Common Issues and Solutions

1. "Module not found" errors:
   - Install missing Python packages: `pip install <package_name>`
   - Check Python environment path

2. Permission denied:
   - Run `chmod +x server.js`
   - Check script directory permissions

3. Server won't start:
   - Verify Node.js version: `node --version`
   - Check MCP SDK installation
   - Validate config file syntax