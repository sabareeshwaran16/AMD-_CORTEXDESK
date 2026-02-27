from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class Decision:
    id: str
    text: str
    owner: Optional[str]
    deadline: Optional[str]
    confidence: float

@dataclass
class ActionItem:
    id: str
    title: str
    description: str
    owner: Optional[str]
    deadline: Optional[str]
    priority: str
    status: str
    source_reference: Optional[str]
    confidence: float

@dataclass
class MeetingOutput:
    source: str
    source_id: str
    timestamp: str
    summary: str
    decisions: List[Decision]
    action_items: List[ActionItem]
    notes: List[str]
    tags: List[str]
    
    def to_dict(self):
        return {
            "source": self.source,
            "source_id": self.source_id,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "decisions": [asdict(d) for d in self.decisions],
            "action_items": [asdict(a) for a in self.action_items],
            "notes": self.notes,
            "tags": self.tags
        }
    
    @classmethod
    def create(cls, source: str, summary: str, decisions: List[dict], 
               action_items: List[dict], notes: List[str] = None, tags: List[str] = None):
        
        source_id = f"{source}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        # Convert decisions
        decision_objs = []
        for i, dec in enumerate(decisions):
            decision_objs.append(Decision(
                id=f"dec_{str(i+1).zfill(3)}",
                text=dec.get("decision", dec.get("text", "")),
                owner=dec.get("owner"),
                deadline=dec.get("deadline"),
                confidence=dec.get("confidence", 0.85)
            ))
        
        # Convert action items
        action_objs = []
        for i, action in enumerate(action_items):
            action_objs.append(ActionItem(
                id=f"task_{str(i+1).zfill(3)}",
                title=action.get("task", action.get("title", ""))[:100],
                description=action.get("task", action.get("description", "")),
                owner=action.get("assignee", action.get("owner")),
                deadline=action.get("deadline"),
                priority=action.get("priority", "Medium").capitalize(),
                status="Pending",
                source_reference=None,
                confidence=action.get("confidence", 0.85)
            ))
        
        return cls(
            source=source,
            source_id=source_id,
            timestamp=timestamp,
            summary=summary,
            decisions=decision_objs,
            action_items=action_objs,
            notes=notes or [],
            tags=tags or []
        )
