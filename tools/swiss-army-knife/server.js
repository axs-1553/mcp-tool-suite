import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { promises as fs } from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SCRIPTS_DIR = "E:\\Artificial Intelligence\\MCP\\swiss-army-files";
const PYTHON_PATH = process.env.PYTHON_PATH || "python";

const HELP_TEXT = `
Swiss Army Knife Tool - Script Creation Guide

1. Script Naming:
   - Files must end with '.sak.py'
   - Example: my-script.sak.py

2. Script Structure:
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
`;

async function getScriptInfo(scriptPath) {
    try {
        // First try reading the file for docstring
        const content = await fs.readFile(scriptPath, 'utf8');
        
        // Look for triple-quoted docstring
        const docMatch = content.match(/"{3}([\s\S]*?"{3})|'{3}([\s\S]*?'{3})/);
        if (docMatch) {
            const docstring = (docMatch[1] || docMatch[2]).replace(/"{3}|'{3}/g, '').trim();
            if (docstring) {
                return docstring;
            }
        }

        // Try running with --info flag as fallback
        return new Promise((resolve) => {
            const process = spawn(PYTHON_PATH, [scriptPath, '--info']);
            let output = '';
            let errorOutput = '';
            
            process.stdout.on('data', (data) => {
                output += data.toString();
            });
            
            process.stderr.on('data', (data) => {
                errorOutput += data.toString();
            });
            
            // Set a timeout to kill the process if it takes too long
            const timeout = setTimeout(() => {
                process.kill();
                resolve(path.basename(scriptPath));
            }, 2000);
            
            process.on('close', (code) => {
                clearTimeout(timeout);
                if (code === 0 && output.trim()) {
                    resolve(output.trim());
                } else {
                    resolve(path.basename(scriptPath));
                }
            });
        });
    } catch (error) {
        console.error(`Error getting script info: ${error.message}`);
        return path.basename(scriptPath);
    }
}

async function loadAvailableScripts() {
    try {
        const files = await fs.readdir(SCRIPTS_DIR);
        const scripts = [];

        for (const file of files) {
            if (file.endsWith('.sak.py')) {
                const fullPath = path.join(SCRIPTS_DIR, file);
                const toolName = path.basename(file, '.sak.py');
                
                try {
                    const description = await getScriptInfo(fullPath);
                    scripts.push({
                        name: toolName,
                        path: fullPath,
                        description: description
                    });
                } catch (error) {
                    console.error(`Error processing script ${file}: ${error.message}`);
                    scripts.push({
                        name: toolName,
                        path: fullPath,
                        description: `Script: ${toolName}`
                    });
                }
            }
        }
        return scripts;
    } catch (error) {
        console.error(`Error loading scripts: ${error.message}`);
        return [];
    }
}

function parseCommandString(commandStr) {
    const parts = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < commandStr.length; i++) {
        const char = commandStr[i];
        
        if (char === '"') {
            inQuotes = !inQuotes;
            continue;
        }
        
        if (char === ' ' && !inQuotes) {
            if (current) {
                parts.push(current);
                current = '';
            }
        } else {
            current += char;
        }
    }
    
    if (current) {
        parts.push(current);
    }
    
    return parts;
}

const server = new Server({
    name: "swiss-army-knife",
    version: "1.0.0"
}, {
    capabilities: {
        tools: {}
    }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [{
        name: "swiss-army-knife",
        description: "Swiss Army Knife tool for running Python scripts. Use --help for script creation guide, --list to see available scripts, --info <script_name> for details.",
        inputSchema: {
            type: "object",
            properties: {
                command: {
                    type: "string",
                    description: "Command to run (--help, --list, --info, or script name)"
                },
                args: {
                    type: "array",
                    items: { type: "string" },
                    description: "Additional arguments for the script"
                }
            },
            required: ["command"]
        }
    }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    
    if (name !== "swiss-army-knife") {
        throw new Error('Invalid tool name');
    }

    try {
        // Parse the command string to handle quoted arguments properly
        const commandParts = parseCommandString(args.command);
        const command = commandParts[0];
        const scriptArgs = [...commandParts.slice(1), ...(args.args || [])];

        if (command === "--help") {
            return {
                content: [{
                    type: "text",
                    text: HELP_TEXT
                }]
            };
        }

        if (command === "--list") {
            const scripts = await loadAvailableScripts();
            return {
                content: [{
                    type: "text",
                    text: JSON.stringify({
                        available_scripts: scripts.map(script => ({
                            name: script.name,
                            description: script.description
                        }))
                    }, null, 2)
                }]
            };
        }

        if (command === "--info") {
            const scriptName = scriptArgs[0];
            if (!scriptName) {
                throw new Error("Script name required for --info");
            }
            const scriptPath = path.join(SCRIPTS_DIR, `${scriptName}.sak.py`);
            const info = await getScriptInfo(scriptPath);
            return {
                content: [{
                    type: "text",
                    text: info
                }]
            };
        }

        // Extract script name and create full path
        const scriptName = command.replace(/\.sak\.py$/, '');
        const scriptPath = path.join(SCRIPTS_DIR, `${scriptName}.sak.py`);
        
        // Verify script exists
        await fs.access(scriptPath);

        // Run the script with arguments
        const process = spawn(PYTHON_PATH, [scriptPath, ...scriptArgs], {
            env: {
                ...process.env,
                PYTHONPATH: SCRIPTS_DIR
            }
        });
        
        return new Promise((resolve, reject) => {
            let stdout = '';
            let stderr = '';

            process.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            process.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            process.on('close', (code) => {
                if (code === 0) {
                    resolve({
                        content: [{
                            type: "text",
                            text: stdout || "Command completed successfully"
                        }]
                    });
                } else {
                    resolve({
                        content: [{
                            type: "text",
                            text: `Error: ${stderr || `Process exited with code ${code}`}`
                        }],
                        isError: true
                    });
                }
            });
        });
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
    console.error("Swiss Army Knife MCP Server running on stdio");
    console.error("Scripts directory:", SCRIPTS_DIR);
}

runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});