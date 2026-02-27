"""
Meeting-related endpoints.
Handles live meeting mode and meeting summaries.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.storage.db import get_db
from app.models import MeetingModel, TaskModel
from app.ai.llm_client import generate

router = APIRouter()


class TranscriptIn(BaseModel):
    title: str | None = None
    transcript: str


def _safe_extract_json_array(text: str) -> list[dict]:
    """
    Try to parse a JSON array from a model response.
    Accepts the whole response being JSON, or JSON embedded inside markdown.
    """
    import json

    text = text.strip()
    # fast path
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
    except Exception:
        pass

    # heuristic: locate first '[' and last ']'
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        snippet = text[start : end + 1]
        try:
            data = json.loads(snippet)
            if isinstance(data, list):
                return [x for x in data if isinstance(x, dict)]
        except Exception:
            return []
    return []


@router.post("/live/start")
async def start_live_meeting():
    """
    Start live meeting mode (capture audio from microphone).
    """
    # TODO: Implement live meeting mode
    return {"message": "Live meeting mode started", "status": "recording"}

@router.post("/live/stop")
async def stop_live_meeting():
    """
    Stop live meeting mode and process captured audio.
    """
    # TODO: Implement stop and processing
    return {"message": "Live meeting mode stopped", "status": "processing"}

@router.get("/summaries")
async def get_meeting_summaries(db: Session = Depends(get_db)):
    """
    Get list of meeting summaries.
    """
    meetings = db.query(MeetingModel).order_by(MeetingModel.created_at.desc()).limit(50).all()
    return {
        "summaries": [
            {
                "id": m.id,
                "title": m.title,
                "created_at": m.created_at.isoformat(),
                "summary": m.summary,
            }
            for m in meetings
        ]
    }


@router.post("/transcript")
async def ingest_transcript(body: TranscriptIn, db: Session = Depends(get_db)):
    """
    Ingest a meeting transcript, summarize it, and extract candidate tasks.

    This is the working path to "meeting mode" without needing microphone/STT yet.
    """
    transcript = (body.transcript or "").strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="transcript cannot be empty")

    # 1) Summarize
    summary = await generate(
        prompt=(
            "Summarize the following meeting transcript in concise bullet points.\n\n"
            f"Transcript:\n{transcript}\n"
        )
    )

    meeting = MeetingModel(title=body.title, transcript=transcript, summary=summary)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    # 2) Extract tasks (best-effort)
    task_resp = await generate(
        prompt=(
            "Extract actionable tasks from the meeting transcript.\n"
            "Return ONLY a JSON array of objects with keys:\n"
            '  - "title" (string)\n'
            '  - "description" (string, optional)\n'
            '  - "due_date" (string, optional)\n'
            '  - "priority" (string, optional)\n\n'
            f"Transcript:\n{transcript}\n"
        )
    )
    tasks_json = _safe_extract_json_array(task_resp)

    created_tasks = []
    for t in tasks_json[:25]:
        title = str(t.get("title", "")).strip()
        if not title:
            continue
        model = TaskModel(
            title=title,
            description=(t.get("description") or None),
            due_date=(t.get("due_date") or None),
            priority=(t.get("priority") or None),
            status="detected",
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        created_tasks.append(
            {
                "id": model.id,
                "title": model.title,
                "description": model.description,
                "due_date": model.due_date,
                "priority": model.priority,
                "status": model.status,
            }
        )

    return {
        "meeting_id": meeting.id,
        "summary": summary,
        "detected_tasks": created_tasks,
    }

