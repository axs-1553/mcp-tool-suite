# GPT-4 MCP Tool

Access OpenAI's GPT-4 through Model Context Protocol.

## Prerequisites
- Node.js v18.x or later
- npm or yarn
- OpenAI API key

## Installation
```bash
npm install @modelcontextprotocol/sdk axios
```

## Configuration
Add to `claude_desktop_config.json`:
```json
{
  "gpt4": {
    "command": "node",
    "args": ["path/to/gpt4-server.js"],
    "type": "module"
  }
}
```

Set environment variable:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Features
- Direct access to GPT-4
- Configurable system messages
- Adjustable response temperature