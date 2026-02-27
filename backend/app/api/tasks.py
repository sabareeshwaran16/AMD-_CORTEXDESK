"""
Task management endpoints.
Handles detected tasks, approvals, and task CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.storage.db import get_db
from app.models import TaskModel

router = APIRouter()

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: Optional[str] = None
    due_date: Optional[str] = None
    scheduled_for: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/")
async def get_tasks(status: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all tasks, optionally filtered by status.
    """
    q = db.query(TaskModel)
    if status:
        q = q.filter(TaskModel.status == status)
    tasks: List[TaskModel] = q.order_by(TaskModel.created_at.desc()).all()
    return {"tasks": [Task.model_validate(t).model_dump() for t in tasks]}

@router.post("/")
async def create_task(task: Task, db: Session = Depends(get_db)):
    """
    Create a new task.
    """
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")

    model = TaskModel(
        title=task.title.strip(),
        description=task.description,
        status=task.status or "pending",
        priority=task.priority,
        due_date=task.due_date,
        scheduled_for=task.scheduled_for,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return {"task": Task.model_validate(model).model_dump()}


@router.patch("/{task_id}")
async def update_task(task_id: int, patch: Task, db: Session = Depends(get_db)):
    """
    Update an existing task.
    """
    model: TaskModel | None = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Task not found")

    if patch.title is not None:
        if not patch.title.strip():
            raise HTTPException(status_code=400, detail="title cannot be empty")
        model.title = patch.title.strip()

    model.description = patch.description
    if patch.status:
        model.status = patch.status
    model.priority = patch.priority
    model.due_date = patch.due_date
    model.scheduled_for = patch.scheduled_for

    db.commit()
    db.refresh(model)
    return {"task": Task.model_validate(model).model_dump()}

@router.post("/approve/{task_id}")
async def approve_task(task_id: int, db: Session = Depends(get_db)):
    """
    Approve a detected task (human-in-the-loop confirmation).
    """
    model: TaskModel | None = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Task not found")
    model.status = "approved"
    db.commit()
    return {"message": f"Task {task_id} approved"}

@router.post("/reject/{task_id}")
async def reject_task(task_id: int, db: Session = Depends(get_db)):
    """
    Reject a detected task.
    """
    model: TaskModel | None = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Task not found")
    model.status = "rejected"
    db.commit()
    return {"message": f"Task {task_id} rejected"}

