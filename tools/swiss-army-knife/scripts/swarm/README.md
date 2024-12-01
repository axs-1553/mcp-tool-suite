# Swarm Framework and Manager

A comprehensive suite for running and managing AI agent swarms through MCP.

## Table of Contents
1. [Core Components](#core-components)
2. [Message Board System](#message-board-system)
3. [Installation and Setup](#installation-and-setup)
4. [Directory Structure](#directory-structure)
5. [Usage Guide](#usage-guide)
6. [State Management](#state-management)
7. [Integration Capabilities](#integration-capabilities)
8. [Best Practices](#best-practices)
9. [Limitations and Weaknesses](#current-limitations-and-weaknesses)
10. [Future Development](#future-development-plan)
11. [Swiss Army Tool Integration](#swiss-army-tool-integration)
12. [Security and Performance](#security-and-performance)

## Core Components

### 1. Swarm Framework (swarm_framework.sak.py)
Core execution engine that:
- Coordinates multiple AI agents
- Handles async task execution
- Manages message passing
- Integrates with GPT-4
- Synthesizes results

### 2. Swarm Manager (swarm-manager.sak.py)
Management interface that:
- Creates and tracks agents
- Monitors agent status
- Persists swarm state
- Combines agent outputs
- Provides status reporting

## Message Board System

The Message Board is a central communication system that facilitates agent coordination and result persistence.

### Message Structure
Each message contains:
- Sender ID (agent or manager)
- Content (task output or command)
- Task ID (for grouping related messages)
- Timestamp
- File path for storage

### Storage System
The Message Board implements:
1. In-memory message queue
2. Persistent JSON storage
3. Individual message files
4. Task-based organization

### Message Flow
1. **Creation**
   - Agent generates output
   - Message object created
   - Timestamp added

2. **Storage**
   - Message added to queue
   - Written to message_board.json
   - Individual file created

3. **Retrieval**
   - Filter by task ID
   - Chronological ordering
   - Load from persistent storage

### Communication Patterns
1. **Agent to Manager**
   - Task completion
   - Status updates
   - Error reporting

2. **Manager to Agent**
   - Task assignments
   - Control commands
   - Configuration updates

## Installation and Setup

### Prerequisites
```bash
# Python dependencies
pip install asyncio
pip install aiohttp
pip install typing_extensions

# For GPT-4 integration
export OPENAI_API_KEY="your-api-key"
```

### Directory Setup
```bash
mkdir -p swarm_outputs
mkdir -p swarm_outputs/agent_outputs
```

## Directory Structure
```
swarm/
├── swarm_framework.sak.py   # Main execution framework
├── swarm-manager.sak.py     # Agent management interface
├── functions.py             # Support functions (GPT-4 integration)
└── swarm_outputs/          # Output directory
    ├── message_board.json   # Framework message history
    ├── swarm_state.json    # Manager state persistence
    └── agent_outputs/      # Individual agent results
```

## Usage Guide

### Basic Framework Operations

1. Execute Single Task
```bash
# Run a task with multiple subtasks
swiss-army-knife swarm_framework --task "Write a blog post" \
  --subtasks \
  "Research current trends in AI" \
  "Draft outline and key points" \
  "Write introduction and body" \
  "Create conclusion and call to action"
```

2. View Task Status
```bash
# List all tasks
swiss-army-knife swarm_framework --list-tasks

# Get specific task messages
swiss-army-knife swarm_framework --get-messages task_12345
```

### Swarm Manager Operations

1. Agent Management
```bash
# Create new agent
swiss-army-knife swarm-manager --create "Generate product descriptions"

# List all agents
swiss-army-knife swarm-manager --list

# Update agent status
swiss-army-knife swarm-manager --update 1 --status running
swiss-army-knife swarm-manager --update 1 --status completed

# Combine agent outputs
swiss-army-knife swarm-manager --combine
```

### Complete Workflow Example
```bash
# 1. Start main task
swiss-army-knife swarm_framework --task "Create marketing campaign" \
  --subtasks \
  "Research target demographics" \
  "Develop messaging strategy" \
  "Design visual elements" \
  "Create content calendar"

# 2. Monitor progress
swiss-army-knife swarm-manager --list

# 3. Update status
swiss-army-knife swarm-manager --update 1 --status completed

# 4. Generate final output
swiss-army-knife swarm-manager --combine
```

## State Management

### Framework State
- Active tasks
- Message history
- Agent assignments
- Task outputs

### Manager State
- Agent registry
- Status tracking
- Output locations
- Task metadata

## Integration Capabilities

### Current Integrations
1. **GPT-4**
   - Direct integration
   - System message support
   - Temperature control

2. **File System**
   - Message persistence
   - Output storage
   - State management

### Planned Integrations
1. **Databases**
   - Message storage
   - State persistence
   - Query capabilities

2. **Monitoring Systems**
   - Performance metrics
   - Status dashboard
   - Alert system

## Best Practices

### 1. Task Design
- Break complex tasks into focused subtasks
- Ensure clear dependencies
- Provide context in task descriptions
- Use consistent naming conventions

### 2. Agent Management
- Monitor agent status regularly
- Update status promptly
- Clean up completed tasks
- Archive important outputs

### 3. Resource Usage
- Limit concurrent agents
- Monitor memory usage
- Clean old message files
- Regular state backups

### 4. Error Handling
- Check task prerequisites
- Validate inputs
- Monitor agent timeouts
- Handle partial failures

### 5. Output Management
- Use descriptive filenames
- Organize by task ID
- Regular cleanup
- Backup important results

## Current Limitations and Weaknesses

1. **Scalability Issues**
   - In-memory message queue limits
   - Single file storage bottlenecks
   - Sequential message processing

2. **Fault Tolerance**
   - No automatic recovery
   - Single point of failure (message board)
   - Limited error handling

3. **Agent Management**
   - Basic lifecycle management
   - No agent prioritization
   - Limited resource control

4. **State Management**
   - File-based persistence only
   - No distributed state
   - Potential race conditions

5. **Task Handling**
   - Linear task execution
   - Limited subtask dependencies
   - No task prioritization

## Future Development Plan

### Phase 1: Robustness
- [ ] Implement distributed message queue
- [ ] Add database backend option
- [ ] Enhance error recovery
- [ ] Improve state persistence

### Phase 2: Scalability
- [ ] Add agent pooling
- [ ] Implement load balancing
- [ ] Support distributed execution
- [ ] Add message compression

### Phase 3: Intelligence
- [ ] Dynamic task prioritization
- [ ] Smart resource allocation
- [ ] Agent specialization
- [ ] Learning from past executions

### Phase 4: Features
- [ ] Real-time monitoring dashboard
- [ ] Advanced task dependencies
- [ ] Agent collaboration patterns
- [ ] Custom agent behaviors

### Phase 5: Integration
- [ ] External system connectors
- [ ] API endpoints
- [ ] Authentication/Authorization
- [ ] Metrics and logging

## Swiss Army Tool Integration

### Current Implementation
- Framework uses GPT-4 for task processing
- Basic tool execution through subprocess
- File-based result handling

### Planned Integration Features

1. **Direct Tool Access**
```python
class EnhancedAgent:
    async def execute_tool(self, tool_name: str, args: dict):
        return await swiss_army.call_tool(tool_name, args)
```

2. **Tool Chain Execution**
```bash
swiss-army-knife swarm_framework --task "Analyze data" \
  --subtasks \
  "process_data:clean_dataset input.csv" \
  "visualize:create_charts processed_data.csv" \
  "analyze:generate_insights charts/"
```

3. **Tool Registry System**
```python
class ToolRegistry:
    def register_tool(self, name: str, capabilities: List[str]):
        self.tools[name] = capabilities

    def find_tool(self, required_capability: str):
        return [t for t in self.tools if required_capability in t.capabilities]
```

### Integration Roadmap
1. **Phase 1: Basic Integration**
   - Tool discovery system
   - Simple tool execution
   - Result parsing

2. **Phase 2: Advanced Features**
   - Tool chaining
   - State management
   - Error handling

3. **Phase 3: Intelligence**
   - Smart tool selection
   - Result optimization
   - Learning from usage

## Security and Performance

### Security Considerations

Current measures:
- Path validation
- Input sanitization
- Basic error handling

Needed improvements:
- Authentication system
- Message encryption
- Access control
- Audit logging

### Performance Optimization

Current bottlenecks:
1. File I/O operations
2. Message serialization
3. Sequential processing
4. Memory usage

Planned optimizations:
1. Batch processing
2. Caching layer
3. Async I/O
4. Resource pooling

## Contributing

Areas where contributions would be most valuable:
1. Scalability improvements
2. Error handling
3. State management
4. Testing framework
5. Documentation

For feature requests or bug reports, please open an issue in the repository.