# Swiss Army Knife MCP Tool

A versatile tool for running Python scripts through the Model Context Protocol.

## Prerequisites
- Node.js v18.x or later
- npm or yarn
- Python 3.x

## Installation

1. Install MCP SDK and dependencies:
```bash
npm install @modelcontextprotocol/sdk glob
```

2. Set your scripts directory:
   - Open server.js
   - Locate the SCRIPTS_DIR constant
   - Update it to your preferred path:
   ```javascript
   const SCRIPTS_DIR = "C:\\Your\\Scripts\\Path";  // Windows
   // or
   const SCRIPTS_DIR = "/your/scripts/path";       // Linux/Mac
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

## Creating Custom Scripts

1. Create a new Python script with `.sak.py` extension in your configured SCRIPTS_DIR
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

## Usage Tips

1. Arguments with spaces can be quoted:
   ```bash
   swiss-army-knife my-script --message "Hello World"
   ```

2. Script Information:
   - Each script should implement the --info flag
   - Use --info to see documentation for any script
   - Use --list to see all available scripts

3. Script Directory:
   - All scripts must be placed in your configured SCRIPTS_DIR
   - Only .sak.py files are recognized
   - Scripts are accessed by their name without the .sak.py extension

## Troubleshooting

1. Script not found:
   - Verify SCRIPTS_DIR path in server.js matches your actual directory
   - Ensure script file exists in the directory
   - Check file extension is `.sak.py`
   - Check file permissions

2. Python errors:
   - Verify Python installation: `python --version`
   - Check script syntax
   - Install any required Python packages for your scripts

3. Argument handling:
   - Use quotes for arguments containing spaces
   - Check script's --info output for expected arguments
   - Verify argument syntax matches script requirements