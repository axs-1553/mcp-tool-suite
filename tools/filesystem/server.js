#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { glob } from 'glob';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const ALLOWED_DIRS = process.argv.slice(2).map(dir => path.resolve(dir));

const DIRECTORY_DESCRIPTIONS = {
    "/path/to/dir1": "Example directory 1",
    "/path/to/dir2": "Example directory 2"
};

const server = new Server({
    name: "filesystem-server",
    version: "1.0.0"
}, {
    capabilities: {
        tools: {}
    }
});

function validatePath(filePath) {
    const normalizedPath = path.normalize(filePath);
    const resolvedPath = path.resolve(normalizedPath);
    return ALLOWED_DIRS.some(dir => resolvedPath.startsWith(dir)) ? resolvedPath : null;
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [{
        name: "filesystem-list",
        description: "List files in a directory",
        inputSchema: {
            type: "object",
            properties: {
                path: { type: "string" }
            }
        }
    }, {
        name: "filesystem-read",
        description: "Read file content",
        inputSchema: {
            type: "object",
            properties: {
                path: { type: "string" }
            },
            required: ["path"]
        }
    }, {
        name: "filesystem-write",
        description: "Write content to file",
        inputSchema: {
            type: "object",
            properties: {
                path: { type: "string" },
                content: { type: "string" }
            },
            required: ["path", "content"]
        }
    }, {
        name: "filesystem-info",
        description: "Get information about allowed directories",
        inputSchema: {
            type: "object",
            properties: {}
        }
    }, {
        name: "filesystem-search",
        description: "Search for files in allowed directories",
        inputSchema: {
            type: "object",
            properties: {
                pattern: { type: "string" },
                recursive: { type: "boolean", default: true }
            },
            required: ["pattern"]
        }
    }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    
    try {
        switch (name) {
            case "filesystem-list": {
                const { path: requestPath = "/" } = args;
                const fullPath = validatePath(requestPath);
                
                if (!fullPath) {
                    throw new Error("Invalid path");
                }

                const files = await fs.readdir(fullPath, { withFileTypes: true });
                return {
                    content: [{
                        type: "text",
                        text: JSON.stringify({
                            files: files.map(file => ({
                                name: file.name,
                                type: file.isDirectory() ? "directory" : "file",
                                path: path.join(requestPath, file.name)
                            }))
                        }, null, 2)
                    }]
                };
            }
            
            case "filesystem-read": {
                const { path: filePath } = args;
                if (!filePath) {
                    throw new Error("Path is required");
                }

                const fullPath = validatePath(filePath);
                if (!fullPath) {
                    throw new Error("Invalid path");
                }

                const content = await fs.readFile(fullPath, "utf-8");
                return {
                    content: [{
                        type: "text",
                        text: content
                    }]
                };
            }
            
            case "filesystem-write": {
                const { path: filePath, content } = args;
                if (!filePath || content === undefined) {
                    throw new Error("Path and content are required");
                }

                const fullPath = validatePath(filePath);
                if (!fullPath) {
                    throw new Error("Invalid path");
                }

                await fs.mkdir(path.dirname(fullPath), { recursive: true });
                await fs.writeFile(fullPath, content, "utf-8");
                return {
                    content: [{
                        type: "text",
                        text: "File written successfully"
                    }]
                };
            }

            case "filesystem-info": {
                const dirInfo = await Promise.all(
                    Object.entries(DIRECTORY_DESCRIPTIONS).map(async ([dirPath, description]) => {
                        try {
                            const stats = await fs.stat(dirPath);
                            return {
                                path: dirPath,
                                description,
                                exists: true,
                                isDirectory: stats.isDirectory(),
                                size: stats.size,
                                modified: stats.mtime
                            };
                        } catch (error) {
                            return {
                                path: dirPath,
                                description,
                                exists: false,
                                error: error.message
                            };
                        }
                    })
                );

                return {
                    content: [{
                        type: "text",
                        text: JSON.stringify(dirInfo, null, 2)
                    }]
                };
            }

            case "filesystem-search": {
                const { pattern, recursive = true } = args;
                const results = [];
                
                for (const dir of ALLOWED_DIRS) {
                    try {
                        const files = await glob(pattern, {
                            cwd: dir,
                            dot: false,
                            absolute: true,
                            recursive: recursive
                        });
                        
                        results.push(...files.filter(file => validatePath(file)));
                    } catch (error) {
                        console.error(`Search error in ${dir}:`, error);
                    }
                }
                
                return {
                    content: [{
                        type: "text",
                        text: JSON.stringify({
                            pattern,
                            matches: results,
                            count: results.length
                        }, null, 2)
                    }]
                };
            }
            
            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    } catch (error) {
        return {
            content: [{
                type: "text",
                text: `Error: ${error.message}`
            }],
            isError: true
        };
    }
});

async function runServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Filesystem MCP Server running on stdio");
    console.error("Allowed directories:", ALLOWED_DIRS);
}

runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});