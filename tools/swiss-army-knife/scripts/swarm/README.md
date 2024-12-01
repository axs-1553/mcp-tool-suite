# Swarm Framework

A sophisticated framework for managing and coordinating AI agents in a swarm architecture. This implementation provides both basic and enhanced functionality for agent management, task execution, and monitoring.

## Components

1. **Base Framework** (`swarm_framework.sak.py`):
   - Core message-passing and task execution
   - GPT-4 integration for agent tasks
   - Asynchronous operations
   - Message board for agent communication

2. **Swarm Manager** (`swarm-manager.sak.py`):
   - Basic agent lifecycle management
   - State persistence
   - Simple output handling
   - Status tracking

3. **Enhanced Framework** (`enhanced-swarm.sak.py` & `enhanced-swarm-daemon.py`):
   - Persistent daemon process for continuous operation
   - Priority-based task scheduling
   - Dependency management
   - Role-based agent organization
   - Performance metrics and monitoring
   - Error logging

## Dependencies

The framework requires the following Python packages:
```
psutil
asyncio
typing
logging
```

Additionally, the framework uses environment-provided functions:
- `gpt4`: For AI agent task execution
- Any other MCP environment functions

## Usage

### Basic Framework
```bash
# Execute a task with subtasks
swiss-army-knife swarm_framework --task "main task" --subtasks "subtask1" "subtask2"

# List all tasks
swiss-army-knife swarm_framework --list-tasks

# Get messages for a specific task
swiss-army-knife swarm_framework --get-messages <task_id>
```

### Swarm Manager
```bash
# Create a new agent
swiss-army-knife swarm-manager --create "task description"

# List all agents
swiss-army-knife swarm-manager --list

# Update agent status
swiss-army-knife swarm-manager --update <id> --status <status>

# Combine outputs
swiss-army-knife swarm-manager --combine
```

### Enhanced Framework
```bash
# Create an agent with priority and role
swiss-army-knife enhanced-swarm --create "task" --task-type high --role worker

# Create an agent with dependencies
swiss-army-knife enhanced-swarm --create "task" --task-type medium --role worker --dependencies 1 2

# View metrics
swiss-army-knife enhanced-swarm --metrics <agent_id>
swiss-army-knife enhanced-swarm --swarm-metrics

# Stop the daemon
swiss-army-knife enhanced-swarm --stop-daemon
```

## Note on GPT-4 Integration

The framework is designed to work within an MCP environment that provides GPT-4 integration via a `gpt4` function. This function is expected to be available in the environment and should accept the following parameters:
- `prompt`: The text prompt for GPT-4
- `temperature`: Controls response randomness (0-1)
- `system_message`: Optional message to set GPT-4's behavior

If you're using this framework outside the MCP environment, you'll need to modify the GPT-4 integration in `swarm_framework.sak.py` to match your environment's AI capabilities.

## Storage and State Management

The framework uses several types of storage:

1. **Message Board Storage**:
   - Location: `swarm_outputs/` directory
   - Contents: Agent messages and task outputs
   - Format: Individual text files and a JSON index

2. **State Files**:
   - `swarm_state.json`: Main state file for agent tracking
   - `daemon.pid`: Daemon process ID file
   - Format: JSON for state, plain text for PID

3. **Agent Outputs**:
   - Named as `agent_<id>_output.txt`
   - Contains individual agent task results
   - Can be combined using the `--combine` option

## Agent Roles and Task Types

### Roles:
- **Coordinator**: Manages task distribution and synchronization
- **Worker**: Executes primary tasks
- **Analyzer**: Processes and analyzes results
- **Monitor**: Tracks system health and performance

### Task Types (Priority Levels):
- **Critical**: Highest priority, immediate execution
- **High**: Important tasks, prioritized execution
- **Medium**: Standard priority level
- **Low**: Background tasks, executed when resources available

## Error Handling and Logging

The framework implements comprehensive error handling:

1. **Daemon Process**:
   - Graceful startup/shutdown
   - Process monitoring
   - Automatic restart on failure

2. **State Management**:
   - Atomic state updates
   - State file corruption protection
   - Automatic state recovery

3. **Logging**:
   - Standard logging levels (INFO, ERROR, etc.)
   - Agent-specific error logs
   - Performance metrics tracking

## Development and Extension

To extend the framework:

1. **Adding New Agent Types**:
   - Extend the `--role` options in `enhanced-swarm.sak.py`
   - Implement role-specific logic in the daemon

2. **Custom Metrics**:
   - Add fields to the metrics dictionary in agent state
   - Implement collection in the daemon process

3. **Integration Points**:
   - GPT-4 integration in `swarm_framework.sak.py`
   - State management in each component
   - Daemon process logic

## Limitations and Considerations

1. **Resource Management**:
   - Monitor system resources when running many agents
   - Consider implementing rate limiting for API calls

2. **State Persistence**:
   - Regular backups recommended
   - Consider implementing state file versioning

3. **Security**:
   - No built-in authentication/authorization
   - Implement access controls if needed
   - Monitor API usage and rate limits
