"""
Scheduler endpoints.
Handles schedule proposals and calendar management.
"""
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.storage.db import get_db
from app.models import TaskModel
from app.scheduler.engine import propose_schedule

router = APIRouter()

@router.get("/proposals")
async def get_schedule_proposals(db: Session = Depends(get_db)):
    """
    Get schedule proposals for tasks.
    """
    # For now propose schedule for all approved/pending tasks without a scheduled slot
    task_ids = [
        t.id
        for t in db.query(TaskModel)
        .filter(TaskModel.status.in_(["approved", "pending"]))
        .filter(TaskModel.scheduled_for.is_(None))
        .all()
    ]
    proposals = propose_schedule(task_ids)
    return {"proposals": proposals}

@router.post("/apply/{proposal_id}")
async def apply_schedule_proposal(proposal_id: int):
    """
    Apply a schedule proposal.
    """
    # TODO: Implement proposal application
    return {"message": f"Schedule proposal {proposal_id} applied"}

