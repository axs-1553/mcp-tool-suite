import argparse
import sys
import json
import time
from pathlib import Path
import subprocess
import logging
import os
import psutil
import atexit
import signal
from datetime import datetime
from typing import List, Optional

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

class SwarmClient:
    def __init__(self):
        self.state_file = Path("swarm_state.json")
        self.daemon_script = Path(__file__).parent / "enhanced-swarm-daemon.py"
        self.daemon_pid_file = Path("daemon.pid")
        self._init_state()
        self.ensure_daemon_running()
        atexit.register(self.cleanup)

    def _init_state(self):
        if not self.state_file.exists():
            with open(self.state_file, 'w') as f:
                json.dump({"agents": {}, "next_id": 1}, f)

    def _is_process_running(self, pid):
        try:
            return psutil.pid_exists(pid)
        except:
            return False

    def cleanup(self):
        if self.daemon_pid_file.exists():
            try:
                with open(self.daemon_pid_file, 'r') as f:
                    pid = int(f.read().strip())
                if self._is_process_running(pid):
                    process = psutil.Process(pid)
                    process.terminate()
                    try:
                        process.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        process.kill()
            except:
                pass
            finally:
                try:
                    self.daemon_pid_file.unlink()
                except:
                    pass

    def ensure_daemon_running(self):
        try:
            with open(self.daemon_pid_file, 'r') as f:
                pid = int(f.read().strip())
                if not self._is_process_running(pid):
                    self._start_daemon()
        except FileNotFoundError:
            self._start_daemon()

    def _start_daemon(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            [sys.executable, str(self.daemon_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        with open(self.daemon_pid_file, 'w') as f:
            f.write(str(process.pid))
        time.sleep(1)

    def load_state(self):
        if self.state_file.exists():
            with open(self.state_file) as f:
                state = json.load(f)
                if isinstance(state.get("agents", {}), list):
                    agents = {str(a["agent_id"]): a for a in state["agents"]}
                    state["agents"] = agents
                return state
        return {"agents": {}, "next_id": 1}

    def save_state(self, state):
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def create_agent(self, task: str, task_type: str, role: str, 
                    dependencies: Optional[List[int]] = None) -> dict:
        state = self.load_state()
        agent_id = state["next_id"]
        
        agent = {
            "agent_id": agent_id,
            "task": task,
            "task_type": task_type,
            "role": role,
            "dependencies": dependencies or [],
            "status": "pending",
            "start_time": datetime.now().isoformat(),
            "completion_time": None,
            "metrics": {},
            "error_log": []
        }
        
        if isinstance(state["agents"], list):
            state["agents"] = {}
        
        state["agents"][str(agent_id)] = agent
        state["next_id"] = agent_id + 1
        self.save_state(state)
        return agent

    def get_agent_metrics(self, agent_id: int) -> Optional[dict]:
        state = self.load_state()
        agent = state["agents"].get(str(agent_id))
        return agent.get("metrics") if agent else None

    def get_swarm_metrics(self) -> dict:
        state = self.load_state()
        agents = state["agents"].values()
        completed = sum(1 for a in agents if a["status"] == "completed")
        failed = sum(1 for a in agents if a["status"] == "failed")
        
        return {
            "total_agents": len(agents),
            "completed": completed,
            "failed": failed,
            "pending": len(agents) - completed - failed,
            "average_execution_time": sum(a["metrics"].get("execution_time", 0) 
                                       for a in agents if a["status"] == "completed") / completed if completed else 0,
            "overall_success_rate": completed / len(agents) if agents else 0
        }

    def combine_outputs(self, output_file: str = "combined_output.txt"):
        state = self.load_state()
        completed_agents = [a for a in state["agents"].values() 
                          if a["status"] == "completed"]
        
        with open(output_file, 'w') as outfile:
            for agent in completed_agents:
                try:
                    with open(f"agent_{agent['agent_id']}_output.txt") as infile:
                        outfile.write(f"\n--- Agent {agent['agent_id']} Output ---\n")
                        outfile.write(infile.read())
                except FileNotFoundError:
                    continue

    def stop_daemon(self):
        try:
            with open(self.daemon_pid_file, 'r') as f:
                pid = int(f.read().strip())
                if self._is_process_running(pid):
                    process = psutil.Process(pid)
                    process.terminate()
                    try:
                        process.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        process.kill()
                    return True
        except:
            pass
        finally:
            try:
                self.daemon_pid_file.unlink()
            except:
                pass
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show script information')
    parser.add_argument('--create', help='Create a new swarm agent with specified task')
    parser.add_argument('--task-type', choices=['critical', 'high', 'medium', 'low'],
                      help='Specify task priority level')
    parser.add_argument('--role', choices=['coordinator', 'worker', 'analyzer', 'monitor'],
                      help='Specify agent role')
    parser.add_argument('--dependencies', type=int, nargs='*',
                      help='Specify agent dependencies (agent IDs)')
    parser.add_argument('--list', action='store_true', help='List all agents and their status')
    parser.add_argument('--metrics', type=int, help='Show metrics for specific agent ID')
    parser.add_argument('--swarm-metrics', action='store_true', help='Show overall swarm metrics')
    parser.add_argument('--combine', action='store_true', help='Combine all completed outputs')
    parser.add_argument('--stop-daemon', action='store_true', help='Stop the swarm daemon')
    args = parser.parse_args()

    if args.info:
        print("""
        Tool Name: Enhanced Swarm Manager (with Daemon)
        Description: Advanced management system for AI agent swarms
        
        Features:
        - Persistent daemon process for task execution
        - Priority-based scheduling
        - Dependency management
        - Role-based organization
        - Performance metrics
        - Error logging
        
        Usage: swiss-army-knife enhanced-swarm [arguments]
        """)
        return

    client = SwarmClient()

    if args.stop_daemon:
        if client.stop_daemon():
            print("Daemon stopped successfully")
        else:
            print("Daemon not running or already stopped")
        return

    if args.create:
        if not args.task_type or not args.role:
            print("Error: --task-type and --role are required when creating an agent")
            return
        
        agent = client.create_agent(args.create, args.task_type, args.role, args.dependencies)
        print(f"Created agent {agent['agent_id']} with task: {agent['task']}")
        print(f"Role: {agent['role']}, Type: {agent['task_type']}")
        if agent['dependencies']:
            print(f"Dependencies: {agent['dependencies']}")

    elif args.list:
        state = client.load_state()
        for agent in state["agents"].values():
            print(f"\nAgent {agent['agent_id']}:")
            print(f"Task: {agent['task']}")
            print(f"Role: {agent['role']}")
            print(f"Type: {agent['task_type']}")
            print(f"Status: {agent['status']}")
            print(f"Started: {agent['start_time']}")
            if agent.get('completion_time'):
                print(f"Completed: {agent['completion_time']}")
            if agent['dependencies']:
                print(f"Dependencies: {agent['dependencies']}")
            if agent['error_log']:
                print("Recent errors:")
                for error in agent['error_log'][-3:]:
                    print(f"  {error['timestamp']}: {error['error']}")

    elif args.metrics is not None:
        metrics = client.get_agent_metrics(args.metrics)
        if metrics:
            print(f"\nMetrics for Agent {args.metrics}:")
            for key, value in metrics.items():
                print(f"{key}: {value}")
        else:
            print(f"No metrics found for agent {args.metrics}")

    elif args.swarm_metrics:
        metrics = client.get_swarm_metrics()
        print("\nSwarm Performance Metrics:")
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")

    elif args.combine:
        client.combine_outputs()
        print("Combined all completed outputs into combined_output.txt")

if __name__ == '__main__':
    main()