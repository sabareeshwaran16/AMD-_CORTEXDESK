from .base_agent import BaseAgent
from typing import Dict, Any, List

class TaskAgent(BaseAgent):
    def __init__(self, event_bus, working_memory, episodic_memory):
        super().__init__(
            agent_id="task_agent",
            capabilities=["synthesize_tasks", "deduplicate", "prioritize"],
            event_bus=event_bus,
            working_memory=working_memory
        )
        self.episodic_memory = episodic_memory
        self.tasks = []
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        actions = task.get("actions", [])
        
        for action in actions:
            if not self._is_duplicate(action):
                priority = self._infer_priority(action)
                action["priority"] = priority
                self.tasks.append(action)
                
                self.episodic_memory.add(
                    event_type="task",
                    content=action["task"],
                    metadata=action
                )
        
        result = {
            "tasks": self.tasks,
            "count": len(self.tasks)
        }
        
        self.publish_event("tasks_synthesized", result)
        return result
    
    def _is_duplicate(self, new_action: Dict[str, Any]) -> bool:
        for existing in self.tasks:
            if self._similarity(new_action["task"], existing["task"]) > 0.8:
                return True
        return False
    
    def _similarity(self, text1: str, text2: str) -> float:
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _infer_priority(self, action: Dict[str, Any]) -> str:
        task = action["task"].lower()
        deadline = action.get("deadline", "")
        
        urgent_keywords = ["urgent", "asap", "immediately", "critical"]
        high_keywords = ["important", "priority", "soon"]
        
        if any(kw in task for kw in urgent_keywords):
            return "urgent"
        elif any(kw in task for kw in high_keywords):
            return "high"
        elif deadline:
            return "medium"
        else:
            return "normal"
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return sorted(self.tasks, key=lambda x: {
            "urgent": 0, "high": 1, "medium": 2, "normal": 3
        }.get(x.get("priority", "normal"), 3))
