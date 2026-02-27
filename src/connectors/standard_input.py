from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

@dataclass
class StandardInput:
    """Standardized input format for all data sources"""
    id: str
    source_type: str  # 'file', 'email', 'meeting', 'manual'
    timestamp: datetime
    raw_text: str
    metadata: Dict[str, Any]
    
    @classmethod
    def create(cls, source_type: str, raw_text: str, metadata: Optional[Dict[str, Any]] = None):
        return cls(
            id=str(uuid.uuid4()),
            source_type=source_type,
            timestamp=datetime.now(),
            raw_text=raw_text,
            metadata=metadata or {}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_type": self.source_type,
            "timestamp": self.timestamp.isoformat(),
            "raw_text": self.raw_text,
            "metadata": self.metadata
        }
