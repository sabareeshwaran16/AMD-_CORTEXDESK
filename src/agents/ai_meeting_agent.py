from .base_agent import BaseAgent
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.human_layer.confirmation import ConfirmationPanel
from src.ai_core.ollama.client import OllamaClient

class AIMeetingAgent(BaseAgent):
    def __init__(self, event_bus, working_memory, confirmation_panel, use_ai=True):
        super().__init__(
            agent_id="ai_meeting_agent",
            capabilities=["extract_actions", "extract_actions_ai", "summarize_ai", "extract_decisions_ai"],
            event_bus=event_bus,
            working_memory=working_memory
        )
        self.confirmation_panel = confirmation_panel
        self.use_ai = use_ai
        self.ollama = OllamaClient() if use_ai else None
        
        # Check if Ollama is available
        if self.use_ai and self.ollama:
            self.ai_available = self.ollama.is_available()
            if not self.ai_available:
                print("⚠️  Ollama not available, falling back to rule-based extraction")
        else:
            self.ai_available = False
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = task.get("text", "")
        source = task.get("source", "")
        
        print(f"[AIMeetingAgent] ===== PROCESSING STARTED =====")
        print(f"[AIMeetingAgent] Processing text from {source}")
        print(f"[AIMeetingAgent] Text length: {len(text)} characters")
        print(f"[AIMeetingAgent] Text preview: {text[:200]}")
        
        actions = []
        decisions = []
        summary = ""
        
        if self.ai_available:
            print("[AIMeetingAgent] Attempting Ollama AI extraction")
            try:
                actions = self.ollama.extract_tasks(text)
                summary_data = self.ollama.summarize_meeting(text)
                summary = summary_data.get("summary", "")
                decisions = summary_data.get("decisions", [])
                decisions = [{"decision": d, "confidence": 0.9} for d in decisions]
                print(f"[AIMeetingAgent] AI extracted {len(actions)} actions, {len(decisions)} decisions")
            except Exception as e:
                print(f"[AIMeetingAgent] AI extraction failed: {e}")
                print(f"[AIMeetingAgent] Falling back to rule-based extraction")
                actions = self._extract_actions_fallback(text)
                decisions = self._extract_decisions_fallback(text)
                summary = self._summarize_fallback(text)
        
        # If AI didn't work or returned nothing, use fallback
        if len(actions) == 0:
            print("[AIMeetingAgent] No actions from AI, using fallback rule-based extraction")
            actions = self._extract_actions_fallback(text)
            decisions = self._extract_decisions_fallback(text)
            summary = self._summarize_fallback(text)
            print(f"[AIMeetingAgent] Fallback extracted {len(actions)} actions, {len(decisions)} decisions")
        
        print(f"[AIMeetingAgent] Adding {len(actions)} actions to confirmation panel")
        # Send actions to confirmation panel
        for i, action in enumerate(actions):
            # Ensure proper format for confirmation panel
            task_data = {
                "task": action.get("task", ""),
                "assignee": action.get("assignee", "unassigned"),
                "deadline": action.get("deadline", ""),
                "priority": action.get("priority", "normal"),
                "confidence": action.get("confidence", 0.85)
            }
            print(f"[AIMeetingAgent] Action {i+1}: {task_data['task'][:50]}...")
            item_id = self.confirmation_panel.add_for_confirmation(
                "task",
                task_data,
                task_data["confidence"]
            )
            print(f"[AIMeetingAgent] Added to confirmation panel with ID: {item_id}")
        
        result = {
            "source": source,
            "actions": actions,
            "decisions": decisions,
            "summary": summary,
            "confidence": 0.9 if self.ai_available else 0.75,
            "ai_powered": self.ai_available,
            "requires_confirmation": True
        }
        
        print(f"[AIMeetingAgent] Publishing meeting_analyzed event")
        self.publish_event("meeting_analyzed", result)
        print(f"[AIMeetingAgent] ===== PROCESSING COMPLETE =====")
        return result
    
    def _extract_actions_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback rule-based extraction"""
        import re
        actions = []
        action_patterns = [
            r"(?:TODO|Action|Task):\s*(.+?)(?:\n|$)",
            r"(\w+)\s+(?:will|should|needs to)\s+(.+?)(?:\n|$)",
            r"@(\w+)\s+(.+?)(?:\n|$)"
        ]
        
        for pattern in action_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    assignee, task = match.groups()
                else:
                    assignee = "unassigned"
                    task = match.group(1)
                
                actions.append({
                    "task": task.strip(),
                    "assignee": assignee.strip(),
                    "deadline": "",
                    "priority": "normal",
                    "confidence": 0.7
                })
        
        return actions
    
    def _extract_decisions_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback rule-based decisions"""
        import re
        from datetime import datetime
        decisions = []
        decision_patterns = [
            r"(?:decided|agreed|concluded):\s*(.+?)(?:\n|$)",
            r"(?:decision|resolution):\s*(.+?)(?:\n|$)"
        ]
        
        for pattern in decision_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                decisions.append({
                    "decision": match.group(1).strip(),
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 0.7
                })
        
        return decisions
    
    def _summarize_fallback(self, text: str) -> str:
        """Fallback summarization"""
        lines = text.split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        
        if len(lines) <= 3:
            return text
        
        return " ".join(lines[:3]) + "..."
