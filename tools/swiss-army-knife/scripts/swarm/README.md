# Swarm Framework and Manager

A comprehensive suite for running and managing AI agent swarms through MCP.

## Components

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

## Installation
```bash
pip install asyncio
```

## Usage

### Running Tasks with the Framework
```bash
# Execute a task with multiple subtasks
swiss-army-knife swarm_framework --task "Write a research paper" \
  --subtasks \
  "Research latest developments" \
  "Analyze current trends" \
  "Write conclusions"

# List all tasks
swiss-army-knife swarm_framework --list-tasks

# Get task messages
swiss-army-knife swarm_framework --get-messages <task_id>
```

### Managing Agents with Swarm Manager
```bash
# Create a new agent
swiss-army-knife swarm-manager --create "Generate creative story"

# List all agents and their status
swiss-army-knife swarm-manager --list

# Update agent status
swiss-army-knife swarm-manager --update 1 --status running

# Combine completed outputs
swiss-army-knife swarm-manager --combine
```

## Directory Structure
```
swarm/
├── swarm_framework.sak.py   # Main execution framework
├── swarm-manager.sak.py     # Agent management interface
├── functions.py            # Support functions (GPT-4 integration)
└── swarm_outputs/         # Output directory
    ├── message_board.json  # Framework message history
    ├── swarm_state.json   # Manager state persistence
    └── agent_outputs/     # Individual agent results
```

## State and Output Files

### Framework Files
- `message_board.json`: Communication history
- `<task_id>_agent_*.txt`: Individual agent outputs
- `<task_id>_manager_*.txt`: Synthesized results

### Manager Files
- `swarm_state.json`: Agent states and metadata
- `agent_*_output.txt`: Individual agent outputs
- `combined_output.txt`: Combined agent results

## Examples

### Complex Task Execution
```bash
# Start with framework for main task
swiss-army-knife swarm_framework --task "Create marketing campaign" \
  --subtasks \
  "Research target audience" \
  "Develop key messages" \
  "Design campaign structure"

# Monitor agents with manager
swiss-army-knife swarm-manager --list

# Update status as agents complete
swiss-army-knife swarm-manager --update 1 --status completed

# Combine final outputs
swiss-army-knife swarm-manager --combine
```

## Workflow Best Practices

1. **Task Planning**
   - Break down complex tasks into clear subtasks
   - Consider dependencies between subtasks
   - Plan agent coordination strategy

2. **Execution**
   - Start with swarm_framework for task distribution
   - Use manager to monitor progress
   - Update agent statuses as they complete

3. **Result Collection**
   - Monitor individual agent outputs
   - Use manager to combine completed work
   - Review synthesized results from framework

## Troubleshooting

1. **Framework Issues**
   - Check message board integrity
   - Verify GPT-4 connectivity
   - Monitor async execution

2. **Manager Issues**
   - Check state file persistence
   - Verify agent status updates
   - Monitor output file creation

3. **Integration Issues**
   - Ensure both components can access shared files
   - Verify output directory permissions
   - Check file naming conventions