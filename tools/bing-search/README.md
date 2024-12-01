# Bing Search MCP Tool

Search the web using Bing's API.

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

## Features
- Web search via Bing API
- Returns formatted results with title, URL, and snippet
- Configurable result count (1-50)