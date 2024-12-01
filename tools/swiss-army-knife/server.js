#!/usr/bin/env node
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

const SCRIPTS_DIR = path.join(__dirname, 'scripts');

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

3. Available Commands:
   - --list: Show all available scripts
   - --info <script_name>: Show script documentation
   - --help: Show this help message
   - <script_name> [args]: Run a specific script

4. Script Location:
   Place scripts in: ${SCRIPTS_DIR}
`;

[Rest of the server.js implementation remains the same as your original file, 
just with SCRIPTS_DIR modified to be relative to server location]