import queue
import threading
from typing import Callable, Dict, List
from datetime import datetime
import json

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = False
        
    def subscribe(self, event_type: str, callback: Callable):
        with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
    
    def publish(self, agent_id: str, event_type: str, payload: dict):
        event = {
            "message_id": f"{agent_id}_{datetime.now().timestamp()}",
            "from_agent": agent_id,
            "event_type": event_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        self.event_queue.put(event)
    
    def start(self):
        self.running = True
        threading.Thread(target=self._process_events, daemon=True).start()
    
    def stop(self):
        self.running = False
    
    def _process_events(self):
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                event_type = event["event_type"]
                
                with self.lock:
                    if event_type in self.subscribers:
                        for callback in self.subscribers[event_type]:
                            try:
                                callback(event)
                            except Exception as e:
                                print(f"Error in callback: {e}")
            except queue.Empty:
                continue
