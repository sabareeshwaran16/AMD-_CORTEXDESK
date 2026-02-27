import requests
import json
from typing import Dict, Any, List, Optional

class OllamaClient:
    """Client for local Ollama LLM"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
    
    def generate(self, prompt: str, system: str = None, temperature: float = 0.7) -> str:
        """Generate text using Ollama"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Ollama error: {e}")
            return ""
    
    def extract_tasks(self, text: str) -> List[Dict[str, Any]]:
        """Extract tasks using AI"""
        system = """You are a task extraction assistant. Extract action items from text.
Return ONLY a JSON array of tasks with this format:
[{"task": "description", "assignee": "name or null", "deadline": "date or null", "priority": "urgent/high/medium/normal"}]"""
        
        prompt = f"""Extract all action items and tasks from this text:

{text}

Return only the JSON array, no other text."""
        
        response = self.generate(prompt, system=system, temperature=0.3)
        
        try:
            # Try to parse JSON from response
            tasks = json.loads(response)
            return tasks if isinstance(tasks, list) else []
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from text
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            return []
    
    def summarize_meeting(self, text: str) -> Dict[str, Any]:
        """Summarize meeting notes"""
        system = """You are a meeting summarization assistant. Create concise summaries.
Return ONLY a JSON object with this format:
{"summary": "brief summary", "key_points": ["point1", "point2"], "decisions": ["decision1"]}"""
        
        prompt = f"""Summarize this meeting:

{text}

Return only the JSON object, no other text."""
        
        response = self.generate(prompt, system=system, temperature=0.5)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            return {"summary": "Summary unavailable", "key_points": [], "decisions": []}
    
    def detect_conflicts(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect conflicts in tasks"""
        system = """You are a conflict detection assistant. Identify scheduling conflicts, duplicate tasks, and issues.
Return ONLY a JSON array of conflicts:
[{"type": "duplicate/deadline_conflict/missing_info", "description": "...", "affected_tasks": [0, 1]}]"""
        
        prompt = f"""Analyze these tasks for conflicts:

{json.dumps(tasks, indent=2)}

Return only the JSON array of conflicts, no other text."""
        
        response = self.generate(prompt, system=system, temperature=0.3)
        
        try:
            conflicts = json.loads(response)
            return conflicts if isinstance(conflicts, list) else []
        except:
            return []
    
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
