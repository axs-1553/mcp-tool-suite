# Filesystem MCP Tool

File system operations through Model Context Protocol with directory access control. This is a different implementation than the default MCP server from Anthropic.

## Prerequisites
- Node.js v18.x or later
- npm or yarn

## Installation
```bash
# Install MCP SDK and dependencies
npm install @modelcontextprotocol/sdk
npm install glob
```

## Configuration
Add to `claude_desktop_config.json`:
```json
{
  "filesystem-server": {
    "command": "node",
    "args": ["path/to/filesystem-server.js", "/allowed/path1", "/allowed/path2"],
    "type": "module"
  }
}
```

## Running the Server
```bash
# Make executable
chmod +x server.js

# Run with allowed directories
./server.js /path1 /path2

# Or via node
node server.js /path1 /path2
```

## Available Tools
- filesystem-list: List directory contents
- filesystem-read: Read file content
- filesystem-write: Write to file
- filesystem-info: Get directory information
- filesystem-search: Search files with pattern matching

## Security
- Access restricted to allowed directories
- Path validation prevents traversal attacks
- Configurable directory permissions
