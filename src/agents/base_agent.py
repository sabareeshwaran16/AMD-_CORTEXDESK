from abc import ABC, abstractmethod
from typing import List, Dict, Any
import threading
import queue

class BaseAgent(ABC):
    def __init__(self, agent_id: str, capabilities: List[str], event_bus, working_memory):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.event_bus = event_bus
        self.working_memory = working_memory
        self.status = "idle"
        self.task_queue = queue.Queue()
        self.running = False
    
    @abstractmethod
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def publish_event(self, event_type: str, payload: Dict[str, Any]):
        self.event_bus.publish(self.agent_id, event_type, payload)
    
    def subscribe(self, event_type: str, callback):
        self.event_bus.subscribe(event_type, callback)
    
    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()
    
    def stop(self):
        self.running = False
    
    def enqueue_task(self, task: Dict[str, Any]):
        self.task_queue.put(task)
    
    def _run(self):
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                self.status = "processing"
                result = self.process(task)
                self.status = "idle"
                
                if result:
                    self.publish_event("task_completed", {
                        "agent_id": self.agent_id,
                        "task": task,
                        "result": result
                    })
            except queue.Empty:
                continue
            except Exception as e:
                self.status = "error"
                self.publish_event("task_failed", {
                    "agent_id": self.agent_id,
                    "error": str(e)
                })

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
    
    def register(self, agent: BaseAgent):
        self.agents[agent.agent_id] = {
            "instance": agent,
            "capabilities": agent.capabilities,
            "status": agent.status
        }
    
    def find_agent_for_capability(self, capability: str) -> BaseAgent:
        for agent_id, info in self.agents.items():
            if capability in info["capabilities"]:
                return info["instance"]
        return None
    
    def get_all_agents(self) -> List[BaseAgent]:
        return [info["instance"] for info in self.agents.values()]
