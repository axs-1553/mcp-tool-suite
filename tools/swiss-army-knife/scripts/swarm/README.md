# Swarm Framework

An asynchronous multi-agent framework that coordinates AI agents to solve complex tasks collaboratively.

## Features
- Asynchronous task execution
- Persistent message board
- Task state management
- Agent coordination
- Result synthesis

## Prerequisites
```bash
pip install asyncio
```

## Core Components

### 1. Message System
- **Message Class**: Handles communication between agents
  - Sender identification
  - Content storage
  - Task tracking
  - Timestamp recording

### 2. Message Board
- **Persistent Storage**: Saves all communication
- **Message Retrieval**: Filter by task ID
- **Structured Output**: Organizes agent outputs

### 3. Swarm Manager
- **Task Coordination**: Manages agent execution
- **Async Operations**: Parallel task processing
- **Result Synthesis**: Combines agent outputs

## Usage

### Basic Task Execution
```bash
swiss-army-knife swarm_framework --task "Write a research paper" \
  --subtasks \
  "Research latest developments in AI" \
  "Analyze current trends" \
  "Write introduction and methodology" \
  "Create conclusions"
```

### View Active Tasks
```bash
swiss-army-knife swarm_framework --list-tasks
```

### Get Task Messages
```bash
swiss-army-knife swarm_framework --get-messages <task_id>
```

### Get Help
```bash
swiss-army-knife swarm_framework --info
```

## Output Structure
```
swarm_outputs/
├── message_board.json           # All messages and task history
├── <task_id>_agent_0_*.txt     # Agent 0's output
├── <task_id>_agent_1_*.txt     # Agent 1's output
└── <task_id>_manager_*.txt     # Final synthesized result
```

## Task Flow
1. **Task Creation**
   - Main task defined
   - Subtasks distributed

2. **Agent Execution**
   - Parallel processing
   - Individual outputs saved

3. **Message Management**
   - Communications logged
   - Results stored

4. **Result Synthesis**
   - Outputs combined
   - Final solution created

## Response Format
```json
{
  "task_id": "unique_id",
  "main_task": "task description",
  "status": "completed",
  "outputs": [
    "path/to/agent0_output.txt",
    "path/to/agent1_output.txt"
  ],
  "final_output": "path/to/final_result.txt"
}
```

## Examples

### Research Project
```bash
swiss-army-knife swarm_framework --task "Research impact of AI on healthcare" \
  --subtasks \
  "Research current AI applications in healthcare" \
  "Analyze effectiveness studies" \
  "Identify future trends" \
  "Compile recommendations"
```

### Content Creation
```bash
swiss-army-knife swarm_framework --task "Create marketing campaign" \
  --subtasks \
  "Research target audience" \
  "Develop key messages" \
  "Design campaign structure" \
  "Create content outline"
```

## Best Practices

1. **Task Division**
   - Keep subtasks focused
   - Ensure clear dependencies
   - Balance workload

2. **Monitoring**
   - Check task status regularly
   - Review agent outputs
   - Track message history

3. **Results Management**
   - Save important outputs
   - Document task IDs
   - Organize by project

## Troubleshooting

1. **Task Execution Issues**
   - Verify subtask clarity
   - Check for dependency conflicts
   - Monitor agent responses

2. **Storage Problems**
   - Check directory permissions
   - Verify file paths
   - Monitor disk space

3. **Message Board Issues**
   - Check JSON integrity
   - Verify message format
   - Clear corrupted entries