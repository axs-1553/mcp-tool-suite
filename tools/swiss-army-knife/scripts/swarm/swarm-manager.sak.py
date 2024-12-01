import argparse
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import threading
import queue

class SwarmAgent:
    def __init__(self, agent_id, task, status="pending"):
        self.agent_id = agent_id
        self.task = task
        self.status = status
        self.start_time = datetime.now()
        self.completion_time = None
        self.output_file = f"agent_{agent_id}_output.txt"
        
    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "task": self.task,
            "status": self.status,
            "start_time": str(self.start_time),
            "completion_time": str(self.completion_time) if self.completion_time else None,
            "output_file": self.output_file
        }

class SwarmManager:
    def __init__(self):
        self.agents = {}
        self.next_id = 1
        self.state_file = Path("swarm_state.json")
        self.load_state()
        
    def load_state(self):
        if self.state_file.exists():
            with open(self.state_file) as f:
                state = json.load(f)
                self.next_id = state.get("next_id", 1)
                for agent_data in state.get("agents", []):
                    agent = SwarmAgent(
                        agent_data["agent_id"],
                        agent_data["task"],
                        agent_data["status"]
                    )
                    self.agents[agent.agent_id] = agent

    def save_state(self):
        state = {
            "next_id": self.next_id,
            "agents": [agent.to_dict() for agent in self.agents.values()]
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def create_agent(self, task):
        agent = SwarmAgent(self.next_id, task)
        self.agents[agent.agent_id] = agent
        self.next_id += 1
        self.save_state()
        return agent

    def update_agent_status(self, agent_id, status):
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            if status == "completed":
                self.agents[agent_id].completion_time = datetime.now()
            self.save_state()

    def list_agents(self):
        return [agent.to_dict() for agent in self.agents.values()]

    def combine_outputs(self, output_file="combined_output.txt"):
        completed_agents = [agent for agent in self.agents.values() 
                          if agent.status == "completed"]
        
        with open(output_file, 'w') as outfile:
            for agent in completed_agents:
                try:
                    with open(agent.output_file) as infile:
                        outfile.write(f"\n--- Agent {agent.agent_id} Output ---\n")
                        outfile.write(infile.read())
                except FileNotFoundError:
                    continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show script information')
    parser.add_argument('--create', help='Create a new swarm agent with specified task')
    parser.add_argument('--list', action='store_true', help='List all agents and their status')
    parser.add_argument('--update', type=int, help='Update agent status (requires --status)')
    parser.add_argument('--status', choices=['pending', 'running', 'completed', 'failed'])
    parser.add_argument('--combine', action='store_true', help='Combine all completed outputs')
    args = parser.parse_args()

    if args.info:
        print("""
        Tool Name: Swarm Manager
        Description: Manages asynchronous AI swarm agents
        Usage: swiss-army-knife swarm-manager [arguments]
        Arguments:
          --create "task": Create new agent with specified task
          --list: Show all agents and their status
          --update ID --status STATUS: Update agent status
          --combine: Combine all completed outputs
        Example:
          swiss-army-knife swarm-manager --create "Generate creative story"
        """)
        return

    manager = SwarmManager()

    if args.create:
        agent = manager.create_agent(args.create)
        print(f"Created agent {agent.agent_id} with task: {agent.task}")

    elif args.list:
        agents = manager.list_agents()
        for agent in agents:
            print(f"\nAgent {agent['agent_id']}:")
            print(f"Task: {agent['task']}")
            print(f"Status: {agent['status']}")
            print(f"Started: {agent['start_time']}")
            if agent['completion_time'] != 'None':
                print(f"Completed: {agent['completion_time']}")

    elif args.update and args.status:
        manager.update_agent_status(args.update, args.status)
        print(f"Updated agent {args.update} status to {args.status}")

    elif args.combine:
        manager.combine_outputs()
        print("Combined all completed outputs into combined_output.txt")

if __name__ == '__main__':
    main()