#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import axios from 'axios';

const server = new Server({
    name: "gpt4",
    version: "1.0.0"
}, {
    capabilities: {
        tools: {}
    }
});

async function callGPT4(prompt, apiKey, systemMessage = "", temperature = 0.7) {
    if (!apiKey) {
        throw new Error('OpenAI API key not found');
    }

    try {
        const response = await axios({
            method: 'post',
            url: 'https://api.openai.com/v1/chat/completions',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            data: {
                model: 'gpt-4',
                messages: [
                    { role: 'system', content: systemMessage || "You are a helpful AI assistant." },
                    { role: 'user', content: prompt }
                ],
                temperature: temperature
            }
        });

        return response.data.choices[0].message.content;
    } catch (error) {
        throw new Error(`GPT-4 request failed: ${error.message}`);
    }
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [{
        name: "gpt4",
        description: "GPT-4 AI Assistant - Provides help with various tasks and queries",
        inputSchema: {
            type: "object",
            properties: {
                prompt: {
                    type: "string",
                    description: "The prompt or question for GPT-4"
                },
                system_message: {
                    type: "string",
                    description: "Optional system message to set GPT-4's behavior",
                    default: "You are a helpful AI assistant."
                },
                temperature: {
                    type: "number",
                    description: "Controls randomness in the response (0-1)",
                    default: 0.7
                }
            },
            required: ["prompt"]
        }
    }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    
    if (name !== "gpt4") {
        throw new Error('Invalid tool name');
    }

    try {
        const result = await callGPT4(
            args.prompt,
            process.env.OPENAI_API_KEY,
            args.system_message,
            args.temperature
        );
        
        return {
            content: [{
                type: "text",
                text: result
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
    console.error("GPT-4 Server running on stdio");
}

runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});