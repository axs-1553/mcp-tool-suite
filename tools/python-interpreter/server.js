#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const server = new Server({
    name: "python-interpreter",
    version: "1.0.0"
}, {
    capabilities: {
        tools: {}
    }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [{
        name: "python-interpreter",
        description: "Execute Python code in a virtual environment",
        inputSchema: {
            type: "object",
            properties: {
                code: {
                    type: "string",
                    description: "Python code to execute"
                },
                venv: {
                    type: "string",
                    description: "Virtual environment name (optional)",
                    default: "default"
                }
            },
            required: ["code"]
        }
    }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name !== "python-interpreter") {
        throw new Error(`Unknown tool: ${request.params.name}`);
    }

    const { code, venv = "default" } = request.params.arguments;
    const venvPath = path.join(__dirname, '.venvs', venv);

    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['-c', code], {
            env: {
                ...process.env,
                VIRTUAL_ENV: venvPath,
                PATH: `${venvPath}\\Scripts;${process.env.PATH}`
            }
        });

        let stdout = '';
        let stderr = '';

        pythonProcess.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                resolve({
                    content: [{
                        type: "text",
                        text: `Error: ${stderr}`
                    }],
                    isError: true
                });
            } else {
                resolve({
                    content: [{
                        type: "text",
                        text: stdout
                    }]
                });
            }
        });
    });
});

async function runServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Python Interpreter MCP Server running on stdio");
}

runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});