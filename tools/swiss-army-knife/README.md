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

2. Configure scripts directory:
Edit server.js to set your SCRIPTS_DIR path where your .sak.py scripts will be stored.

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

## Included Tools

### Data Visualization Suite
Located in `scripts/viz/`

1. visualize.sak.py: Main visualization tool
   - Supports multiple plot types: line, bar, scatter, box, violin, heatmap, pie, area, radar, donut
   - Features:
     - Multiple subplots with --subplots and --layout
     - Custom color palettes with --palette
     - Stacked charts with --stacked
     - Data insights with --insights
     - Interactive plots with --interactive

2. Dependencies:
   ```bash
   cd scripts/viz
   pip install -r requirements.txt
   ```

3. Example Usage:
   ```bash
   swiss-army-knife visualize data.csv output.png --type bar --x category --y value
   swiss-army-knife visualize data.csv viz.html --interactive --insights --subplots "scatter;x=x;y=y|bar;x=category;y=value"
   ```

## Creating Custom Scripts

1. Create a new Python script with `.sak.py` extension in your scripts directory
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
   - Verify SCRIPTS_DIR path in server.js matches your actual directory
   - Check file extension is `.sak.py`
   - Check file permissions

2. Python errors:
   - Check Python installation: `python --version`
   - Verify script syntax
   - Install required packages for specific scripts

3. Visualization tool issues:
   - Install all required Python packages: `pip install -r scripts/viz/requirements.txt`
   - Check input data format (CSV or JSON)
   - Verify column names match your data