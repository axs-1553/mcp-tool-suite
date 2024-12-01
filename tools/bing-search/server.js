#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import fetch from 'node-fetch';

const server = new Server({
    name: "bing-search",
    version: "1.0.0"
}, {
    capabilities: {
        tools: {}
    }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [{
        name: "bing-search",
        description: "Search the web using Bing",
        inputSchema: {
            type: "object",
            properties: {
                query: {
                    type: "string",
                    description: "Search query"
                },
                count: {
                    type: "number",
                    description: "Number of results (1-50)",
                    minimum: 1,
                    maximum: 50,
                    default: 10
                }
            },
            required: ["query"]
        }
    }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name !== "bing-search") {
        throw new Error(`Unknown tool: ${request.params.name}`);
    }

    const { query, count = 10 } = request.params.arguments;
    const url = `https://api.bing.microsoft.com/v7.0/search?q=${encodeURIComponent(query)}&count=${count}`;

    try {
        const response = await fetch(url, {
            headers: {
                'Ocp-Apim-Subscription-Key': process.env.BING_API_KEY
            }
        });

        if (!response.ok) {
            throw new Error(`Bing API error: ${response.statusText}`);
        }

        const data = await response.json();
        return {
            content: [{
                type: "text",
                text: JSON.stringify(data, null, 2)
            }]
        };
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
    console.error("Bing Search MCP Server running on stdio");
}

runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});