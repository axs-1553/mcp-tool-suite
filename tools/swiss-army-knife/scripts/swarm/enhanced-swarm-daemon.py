import time
import json
from pathlib import Path
import logging
import multiprocessing
from datetime import datetime
import random
import signal
import sys
import atexit

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

class SwarmDaemon:
    def __init__(self):
        self.state_file = Path("swarm_state.json")
        self.running = True
        self.load_state()
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        atexit.register(self.cleanup)
        
    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    self.state = json.load(f)
                    if isinstance(self.state.get("agents", {}), list):
                        agents = {str(a["agent_id"]): a for a in self.state["agents"]}
                        self.state["agents"] = agents
            except Exception as e:
                logging.error(f"Error loading state: {str(e)}")
                self.state = {"agents": {}, "next_id": 1}
        else:
            self.state = {"agents": {}, "next_id": 1}

    def save_state(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving state: {str(e)}")

    def process_agent(self, agent_id):
        agent = self.state["agents"].get(str(agent_id))
        if not agent:
            return

        dependencies_met = all(
            self.state["agents"].get(str(dep_id), {}).get("status") == "completed"
            for dep_id in agent.get("dependencies", [])
        )

        if agent["status"] == "pending" and dependencies_met:
            agent["status"] = "running"
            self.save_state()

            # Simulate task execution
            time.sleep(random.uniform(0.5, 2.0))
            success = random.random() > 0.1

            if success:
                with open(f"agent_{agent_id}_output.txt", 'w') as f:
                    f.write(f"Task execution results for agent {agent_id}\n")
                    f.write(f"Task: {agent['task']}\n")
                    f.write(f"Role: {agent['role']}\n")
                    f.write(f"Execution successful")

                agent["status"] = "completed"
                agent["completion_time"] = datetime.now().isoformat()
                agent["metrics"] = {
                    "execution_time": random.uniform(0.5, 2.0),
                    "memory_usage": random.uniform(50, 200),
                    "success_rate": 1.0,
                    "iterations": 1
                }
            else:
                agent["status"] = "failed"
                agent["error_log"].append({
                    "timestamp": datetime.now().isoformat(),
                    "error": "Task execution failed"
                })

            self.save_state()

    def cleanup(self):
        logging.info("Cleaning up daemon resources...")
        self.running = False
        self.save_state()

    def run(self):
        logging.info("Swarm daemon started")
        while self.running:
            for agent_id in list(self.state["agents"].keys()):
                try:
                    self.process_agent(agent_id)
                except Exception as e:
                    logging.error(f"Error processing agent {agent_id}: {str(e)}")
            time.sleep(0.1)

    def handle_shutdown(self, signum, frame):
        logging.info("Shutting down swarm daemon...")
        self.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    daemon = SwarmDaemon()
    daemon.run()