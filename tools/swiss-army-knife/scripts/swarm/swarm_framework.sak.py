import argparse
import asyncio
import json
import uuid
import os
from typing import List, Dict, Any
from datetime import datetime
from functions import gpt4

class Message:
    def __init__(self, sender: str, content: str, task_id: str):
        self.sender = sender
        self.content = content
        self.task_id = task_id
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, str]:
        return {
            "sender": self.sender,
            "content": self.content,
            "task_id": self.task_id,
            "timestamp": self.timestamp
        }

class MessageBoard:
    def __init__(self, storage_path: str = "E:/Artificial Intelligence/MCP/swiss-army-files/swarm_outputs"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.messages: List[Message] = []
        self.load_messages()

    def load_messages(self):
        try:
            with open(os.path.join(self.storage_path, "message_board.json"), 'r') as f:
                data = json.load(f)
                self.messages = [Message(**msg) for msg in data]
        except FileNotFoundError:
            self.messages = []

    def save_messages(self):
        with open(os.path.join(self.storage_path, "message_board.json"), 'w') as f:
            json.dump([msg.to_dict() for msg in self.messages], f)

    def post_message(self, message: Message):
        self.messages.append(message)
        self.save_messages()
        
        filename = f"{message.task_id}_{message.sender}_{message.timestamp}.txt"
        filepath = os.path.join(self.storage_path, filename)
        with open(filepath, 'w') as f:
            f.write(message.content)
        return filepath

    def get_messages(self, task_id: str = None) -> List[Message]:
        if task_id:
            return [m for m in self.messages if m.task_id == task_id]
        return self.messages

class SwarmManager:
    def __init__(self):
        self.message_board = MessageBoard()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}

    async def execute_agent_task(self, task: str, task_id: str, agent_id: str):
        response = gpt4(
            prompt=task,
            temperature=0.7,
            system_message=f"You are Agent {agent_id} in the swarm. Complete your assigned subtask efficiently."
        )
        
        filepath = self.message_board.post_message(
            Message(f"agent_{agent_id}", response['response'], task_id)
        )
        return {"response": response['response'], "filepath": filepath}

    async def execute_task(self, main_task: str, subtasks: List[str]) -> Dict[str, Any]:
        task_id = str(uuid.uuid4())[:8]
        self.active_tasks[task_id] = {
            "main_task": main_task,
            "subtasks": subtasks,
            "status": "in_progress",
            "outputs": []
        }

        tasks = [
            self.execute_agent_task(subtask, task_id, f"{i}")
            for i, subtask in enumerate(subtasks)
        ]
        
        results = await asyncio.gather(*tasks)
        
        synthesis_prompt = f"""Main task: {main_task}
Results from agents:
{json.dumps([r['response'] for r in results], indent=2)}
Synthesize these results into a complete solution."""

        final_result = gpt4(
            prompt=synthesis_prompt,
            temperature=0.5,
            system_message="You are the swarm manager. Create a cohesive solution."
        )

        final_filepath = self.message_board.post_message(
            Message("manager", final_result['response'], task_id)
        )

        self.active_tasks[task_id].update({
            "status": "completed",
            "outputs": [r["filepath"] for r in results],
            "final_output": final_filepath
        })
        
        return self.active_tasks[task_id]

def main():
    parser = argparse.ArgumentParser(description='Swarm Framework')
    parser.add_argument('--info', action='store_true', help='Show script information')
    parser.add_argument('--task', type=str, help='Main task description')
    parser.add_argument('--subtasks', nargs='+', help='List of subtasks')
    parser.add_argument('--list-tasks', action='store_true', help='List all tasks')
    parser.add_argument('--get-messages', type=str, help='Get messages for task ID')
    
    args = parser.parse_args()

    if args.info:
        print("""
        Swarm Framework
        Description: Coordinates multiple AI agents working on subtasks in parallel
        
        Usage: 
        swiss-army-knife swarm_framework --task "main task" --subtasks "subtask1" "subtask2"
        swiss-army-knife swarm_framework --list-tasks
        swiss-army-knife swarm_framework --get-messages <task_id>
        
        Outputs saved to: E:/Artificial Intelligence/MCP/swiss-army-files/swarm_outputs/
        """)
        return

    manager = SwarmManager()
    
    if args.task and args.subtasks:
        result = asyncio.run(manager.execute_task(args.task, args.subtasks))
        print(json.dumps(result, indent=2))
        
    elif args.list_tasks:
        print(json.dumps(manager.active_tasks, indent=2))
        
    elif args.get_messages:
        messages = manager.message_board.get_messages(args.get_messages)
        print(json.dumps([m.to_dict() for m in messages], indent=2))

if __name__ == '__main__':
    main()