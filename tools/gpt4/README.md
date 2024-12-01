# GPT-4 MCP Tool

Access OpenAI's GPT-4 through Model Context Protocol. Coded to use GPT-4o-mini but any model can be used.

## Prerequisites
- Node.js v18.x or later
- npm or yarn
- OpenAI API key

## Installation
```bash
# Install MCP SDK and dependencies
npm install @modelcontextprotocol/sdk
npm install axios
```

## Configuration
Add to `claude_desktop_config.json`:
```json
{
  "gpt4-analyze": {
    "command": "node",
    "args": ["path/to/gpt4-server.js"],
    "type": "module",
    "env": {
      "OPENAI_API_KEY": "your-api-key"
    }
  }
}
```

## Running the Server
```bash
# Make executable
chmod +x server.js

# Run directly
./server.js

# Or via node
node server.js
```

## Features
- Direct access to GPT-4
- Configurable system messages
- Adjustable response temperature (0-1)
