from .base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime
from dateutil import parser as date_parser

class ConflictDetectorAgent(BaseAgent):
    def __init__(self, event_bus, working_memory, ollama_client=None):
        super().__init__(
            agent_id="conflict_detector",
            capabilities=["detect_conflicts", "find_duplicates", "check_deadlines"],
            event_bus=event_bus,
            working_memory=working_memory
        )
        self.ollama = ollama_client
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        tasks = task.get("tasks", [])
        
        conflicts = []
        
        # Detect duplicates
        conflicts.extend(self._detect_duplicates(tasks))
        
        # Detect deadline conflicts
        conflicts.extend(self._detect_deadline_conflicts(tasks))
        
        # Detect missing information
        conflicts.extend(self._detect_missing_info(tasks))
        
        # Use AI if available
        if self.ollama and self.ollama.is_available():
            ai_conflicts = self.ollama.detect_conflicts(tasks)
            conflicts.extend(ai_conflicts)
        
        result = {
            "conflicts": conflicts,
            "count": len(conflicts)
        }
        
        self.publish_event("conflicts_detected", result)
        return result
    
    def _detect_duplicates(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect duplicate tasks"""
        conflicts = []
        
        for i, task1 in enumerate(tasks):
            for j, task2 in enumerate(tasks[i+1:], i+1):
                similarity = self._calculate_similarity(
                    task1.get("task", ""),
                    task2.get("task", "")
                )
                
                if similarity > 0.8:
                    conflicts.append({
                        "type": "duplicate",
                        "description": f"Possible duplicate tasks detected",
                        "affected_tasks": [i, j],
                        "severity": "medium",
                        "tasks": [task1.get("task"), task2.get("task")]
                    })
        
        return conflicts
    
    def _detect_deadline_conflicts(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect overlapping deadlines"""
        conflicts = []
        
        # Group tasks by assignee and deadline
        assignee_deadlines = {}
        
        for i, task in enumerate(tasks):
            assignee = task.get("assignee", "").lower()
            deadline = task.get("deadline", "")
            
            if not assignee or not deadline or assignee == "unassigned":
                continue
            
            try:
                deadline_date = date_parser.parse(deadline, fuzzy=True)
                
                if assignee not in assignee_deadlines:
                    assignee_deadlines[assignee] = []
                
                assignee_deadlines[assignee].append({
                    "index": i,
                    "date": deadline_date,
                    "task": task
                })
            except:
                continue
        
        # Check for same-day conflicts
        for assignee, task_list in assignee_deadlines.items():
            task_list.sort(key=lambda x: x["date"])
            
            for i in range(len(task_list) - 1):
                if task_list[i]["date"].date() == task_list[i+1]["date"].date():
                    conflicts.append({
                        "type": "deadline_conflict",
                        "description": f"{assignee} has multiple tasks due on the same day",
                        "affected_tasks": [task_list[i]["index"], task_list[i+1]["index"]],
                        "severity": "high",
                        "assignee": assignee,
                        "date": task_list[i]["date"].strftime("%Y-%m-%d")
                    })
        
        return conflicts
    
    def _detect_missing_info(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect tasks with missing information"""
        conflicts = []
        
        for i, task in enumerate(tasks):
            missing = []
            
            if not task.get("assignee") or task.get("assignee") == "unassigned":
                missing.append("assignee")
            
            if not task.get("deadline"):
                missing.append("deadline")
            
            if missing:
                conflicts.append({
                    "type": "missing_info",
                    "description": f"Task missing: {', '.join(missing)}",
                    "affected_tasks": [i],
                    "severity": "low",
                    "missing_fields": missing,
                    "task": task.get("task", "")
                })
        
        return conflicts
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
