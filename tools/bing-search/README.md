# Bing Search MCP Tool

Search the web using Bing's API through Model Context Protocol.

## Prerequisites
- Node.js v18.x or later
- npm or yarn

## Installation
```bash
# Install MCP SDK dependencies
npm install @modelcontextprotocol/sdk

# Install tool dependencies
npm install axios
```

## Setup
1. Get a Bing API key from [Microsoft Azure Portal](https://portal.azure.com)
2. Set environment variable: `BING_API_KEY`

## Configuration

Add to your `claude_desktop_config.json`:
```json
{
  "bing-search": {
    "command": "node",
    "args": ["path/to/bing-search-server.js"],
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

## Features
- Web search via Bing API
- Returns formatted results with title, URL, and snippet
- Configurable result count (1-50)