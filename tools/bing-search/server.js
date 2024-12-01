#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";

const BING_API_KEY = process.env.BING_API_KEY;
if (!BING_API_KEY) {
    throw new Error("BING_API_KEY environment variable is required");
}

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

    try {
        const response = await axios.get('https://api.bing.microsoft.com/v7.0/search', {
            headers: {
                'Ocp-Apim-Subscription-Key': BING_API_KEY
            },
            params: {
                q: query,
                count: count
            }
        });

        const results = response.data.webPages.value.map(page => ({
            title: page.name,
            url: page.url,
            snippet: page.snippet
        }));

        return {
            content: [{
                type: "text",
                text: JSON.stringify(results, null, 2)
            }]
        };
    } catch (error) {
        return {
            content: [{
                type: "text",
                text: `Search error: ${error.message}`
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