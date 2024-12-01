import subprocess
import json
from typing import Dict, Any

def gpt4(prompt: str, system_message: str = None, temperature: float = 0.7) -> Dict[str, Any]:
    """
    Call GPT-4 using the swiss-army-knife GPT4 tool
    """
    request = {
        "command": "gpt4",
        "args": ["--prompt", prompt]
    }
    
    if system_message:
        request["args"].extend(["--system_message", system_message, "--temperature", str(temperature)])

    try:
        result = subprocess.run(
            ["swiss-army-knife", json.dumps(request)],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                return {
                    "response": response['content'][0]['text'],
                    "status": "success"
                }
            except:
                return {
                    "response": result.stdout,
                    "status": "success"
                }
        else:
            return {
                "response": f"Error: {result.stderr}",
                "status": "error"
            }
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "status": "error"
        }