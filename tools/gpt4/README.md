# GPT-4 MCP Tool

Access OpenAI's GPT-4 through Model Context Protocol.

## Installation
```bash
npm install @modelcontextprotocol/sdk axios
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