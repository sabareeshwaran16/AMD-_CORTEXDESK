from .base_agent import BaseAgent
from typing import Dict, Any, List
import re
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.human_layer.confirmation import ConfirmationPanel
from src.connectors.structured_output import MeetingOutput

class MeetingAgent(BaseAgent):
    def __init__(self, event_bus, working_memory, confirmation_panel):
        super().__init__(
            agent_id="meeting_agent",
            capabilities=["extract_actions", "summarize", "extract_decisions"],
            event_bus=event_bus,
            working_memory=working_memory
        )
        self.confirmation_panel = confirmation_panel
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = task.get("text", "")
        source = task.get("source", "manual")
        
        print(f"[MeetingAgent] Processing text from {source}")
        print(f"[MeetingAgent] Text length: {len(text)}")
        
        actions = self._extract_actions(text)
        decisions = self._extract_decisions(text)
        summary = self._summarize(text)
        notes = self._extract_notes(text)
        tags = self._extract_tags(text)
        
        print(f"[MeetingAgent] Found {len(actions)} actions, {len(decisions)} decisions")
        
        # Create structured output
        meeting_output = MeetingOutput.create(
            source=source,
            summary=summary,
            decisions=decisions,
            action_items=actions,
            notes=notes,
            tags=tags
        )
        
        # Send action items to confirmation panel
        for action in meeting_output.action_items:
            print(f"[MeetingAgent] Adding to confirmation: {action.title}")
            self.confirmation_panel.add_for_confirmation(
                "task",
                {
                    "id": action.id,
                    "task": action.title,
                    "description": action.description,
                    "assignee": action.owner,
                    "deadline": action.deadline,
                    "priority": action.priority,
                    "confidence": action.confidence
                },
                action.confidence
            )
        
        result = meeting_output.to_dict()
        result["requires_confirmation"] = True
        
        self.publish_event("meeting_analyzed", result)
        return result
    
    def _extract_actions(self, text: str) -> List[Dict[str, Any]]:
        actions = []
        lines = text.split('\n')
        
        # Pattern 1: "Person needs to/will/should do something"
        pattern1 = r'([A-Z][a-z]+)\s+(?:needs to|will|should|must)\s+(.+?)(?:\s+by\s+([\w\s]+))?(?:\.|$)'
        
        # Pattern 2: "Action: something" or "TODO: something"
        pattern2 = r'(?:Action|TODO|Task):\s*(.+?)(?:\.|$)'
        
        # Pattern 3: Lines starting with bullet points or dashes
        pattern3 = r'^[\s]*[-•*]\s*(.+?)(?:\.|$)'
        
        for line in lines:
            line = line.strip()
            if len(line) < 10 or len(line) > 200:  # Skip too short or too long
                continue
                
            # Try pattern 1
            match = re.search(pattern1, line, re.IGNORECASE)
            if match:
                assignee, task, deadline = match.groups()
                actions.append({
                    "task": task.strip(),
                    "assignee": assignee.strip(),
                    "deadline": deadline.strip() if deadline else "",
                    "confidence": 0.85
                })
                continue
            
            # Try pattern 2
            match = re.search(pattern2, line, re.IGNORECASE)
            if match:
                task = match.group(1).strip()
                assignee_match = re.search(r'([A-Z][a-z]+)\s+', task)
                assignee = assignee_match.group(1) if assignee_match else "unassigned"
                actions.append({
                    "task": task,
                    "assignee": assignee,
                    "deadline": "",
                    "confidence": 0.8
                })
                continue
            
            # Try pattern 3 - bullet points
            match = re.search(pattern3, line)
            if match and any(keyword in line.lower() for keyword in ['complete', 'review', 'prepare', 'schedule', 'send', 'update', 'create', 'implement']):
                task = match.group(1).strip()
                assignee_match = re.search(r'([A-Z][a-z]+)\s+', task)
                assignee = assignee_match.group(1) if assignee_match else "unassigned"
                actions.append({
                    "task": task,
                    "assignee": assignee,
                    "deadline": "",
                    "confidence": 0.75
                })
        
        # Limit to top 10 most relevant actions
        return actions[:10]
    
    def _extract_decisions(self, text: str) -> List[Dict[str, Any]]:
        decisions = []
        lines = text.split('\n')
        
        decision_keywords = ['decided', 'agreed', 'approved', 'concluded', 'resolved', 'decision']
        
        for line in lines:
            line = line.strip()
            if len(line) < 10 or len(line) > 150:  # Skip too short or too long
                continue
            
            if any(keyword in line.lower() for keyword in decision_keywords):
                # Extract the decision part
                for keyword in decision_keywords:
                    if keyword in line.lower():
                        parts = re.split(keyword, line, flags=re.IGNORECASE)
                        if len(parts) > 1:
                            decision_text = parts[1].strip(' :-').strip()
                            if decision_text:
                                decisions.append({
                                    "decision": decision_text,
                                    "timestamp": datetime.now().isoformat(),
                                    "confidence": 0.8
                                })
                                break
        
        return decisions[:5]  # Limit to 5 decisions
    
    def _summarize(self, text: str) -> str:
        lines = text.split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        
        if len(lines) <= 3:
            return text
        
        return " ".join(lines[:3]) + "..."
    
    def _extract_notes(self, text: str) -> List[str]:
        """Extract notable mentions or comments"""
        import re
        notes = []
        
        # Look for lines with "mentioned", "suggested", "noted"
        pattern = r'(.+?(?:mentioned|suggested|noted|said).+?)(?:\n|$)'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            notes.append(match.group(1).strip())
        
        return notes[:5]  # Limit to 5 notes
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text"""
        tags = set()
        
        # Common project-related keywords
        keywords = ['project', 'research', 'deadline', 'meeting', 'review', 
                   'budget', 'proposal', 'design', 'development', 'testing']
        
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                tags.add(keyword)
        
        return list(tags)[:5]  # Limit to 5 tags
    
    def _extract_deadline(self, text: str) -> str:
        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\d{2}/\d{2}/\d{4}",
            r"(?:by|before|until)\s+(\w+\s+\d+)"
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
