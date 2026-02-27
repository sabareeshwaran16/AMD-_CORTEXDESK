from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class ConfirmationPanel:
    """Human-in-the-loop confirmation system"""
    
    def __init__(self, storage_path: str = "data/pending_confirmations.json"):
        self.storage_path = storage_path
        self.pending_items = []
    
    def add_for_confirmation(self, item_type: str, data: Dict[str, Any], confidence: float) -> str:
        """Add item requiring human confirmation"""
        item = {
            "id": f"{item_type}_{datetime.now().timestamp()}",
            "type": item_type,
            "data": data,
            "confidence": confidence,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.pending_items.append(item)
        print(f"[ConfirmationPanel] Added item: {item['id']} - {data.get('task', 'N/A')[:50]}")
        self._save()
        print(f"[ConfirmationPanel] Total pending: {len(self.get_pending())}")
        return item["id"]
    
    def get_pending(self, item_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all pending confirmations"""
        if item_type:
            return [item for item in self.pending_items if item["type"] == item_type and item["status"] == "pending"]
        return [item for item in self.pending_items if item["status"] == "pending"]
    
    def approve(self, item_id: str, edited_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Approve an item (with optional edits)"""
        for item in self.pending_items:
            if item["id"] == item_id:
                item["status"] = "approved"
                item["approved_at"] = datetime.now().isoformat()
                if edited_data:
                    item["data"] = edited_data
                    item["edited"] = True
                self._save()
                return item
        raise ValueError(f"Item {item_id} not found")
    
    def reject(self, item_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Reject an item"""
        for item in self.pending_items:
            if item["id"] == item_id:
                item["status"] = "rejected"
                item["rejected_at"] = datetime.now().isoformat()
                if reason:
                    item["rejection_reason"] = reason
                self._save()
                return item
        raise ValueError(f"Item {item_id} not found")
    
    def get_approved(self) -> List[Dict[str, Any]]:
        """Get all approved items"""
        return [item for item in self.pending_items if item["status"] == "approved"]
    
    def clear_processed(self):
        """Remove approved/rejected items"""
        self.pending_items = [item for item in self.pending_items if item["status"] == "pending"]
        self._save()
    
    def _save(self):
        """Save to disk"""
        import os
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.pending_items, f, indent=2)
    
    def _load(self):
        """Load from disk"""
        try:
            with open(self.storage_path, 'r') as f:
                self.pending_items = json.load(f)
        except FileNotFoundError:
            self.pending_items = []
