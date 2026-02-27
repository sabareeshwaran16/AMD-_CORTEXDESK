"""
File ingestion endpoints.
Handles uploading and processing documents.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from typing import List

from pathlib import Path
import uuid
import re
from datetime import datetime

from app.core.config import settings
from app.connectors.file_reader import read_file
from app.preprocessing.chunking import chunk_text
from app.storage.vector_store import VectorStore
from app.ai.llm_client import generate
from app.models import TaskModel
from app.storage.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


def _sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and handle special characters."""
    # Remove path separators and dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    # Ensure filename is not empty
    if not filename:
        filename = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return filename


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


async def _process_and_index_file(file_path: Path, original_name: str, db: Session):
    """
    Read a file, chunk it, embed it, store chunks in the vector DB,
    and extract tasks automatically.
    """
    text = await run_in_threadpool(read_file, file_path)
    if not text:
        return 0, []

    chunks = chunk_text(text)
    store = VectorStore()

    metadatas = []
    ids = []
    for idx, chunk in enumerate(chunks):
        chunk_id = f"{uuid.uuid4()}-{idx}"
        ids.append(chunk_id)
        metadatas.append(
            {
                "source": original_name,
                "vault_path": str(file_path),
                "chunk_index": idx,
            }
        )

    await run_in_threadpool(store.add_documents, chunks, metadatas, ids)

    # Extract tasks from document using LLM
    extracted_tasks = []
    try:
        task_resp = await generate(
            prompt=(
                "Extract actionable tasks from the following document content.\n"
                "Return ONLY a JSON array of objects with keys:\n"
                '  - "title" (string, required)\n'
                '  - "description" (string, optional)\n'
                '  - "due_date" (string, optional, ISO format if mentioned)\n'
                '  - "priority" (string, optional: "high", "medium", "low")\n\n'
                f"Document content (first 3000 chars):\n{text[:3000]}\n"
            )
        )
        tasks_json = _safe_extract_json_array(task_resp)

        for t in tasks_json[:25]:  # Limit to 25 tasks per document
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
            extracted_tasks.append(
                {
                    "id": model.id,
                    "title": model.title,
                    "description": model.description,
                    "due_date": model.due_date,
                    "priority": model.priority,
                    "status": model.status,
                }
            )
    except Exception as exc:
        # If task extraction fails, still return success for indexing
        pass

    return len(chunks), extracted_tasks


@router.post("/files")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """
    Upload and ingest files (PDF, DOCX, XLSX, TXT, PPTX).
    Files are processed locally, indexed into vector DB, and tasks are automatically extracted.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Validate file types
    allowed_extensions = {'.pdf', '.docx', '.xlsx', '.pptx', '.txt'}
    for f in files:
        if f.filename:
            ext = Path(f.filename).suffix.lower()
            if ext not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {ext}. Allowed: {', '.join(allowed_extensions)}"
                )

    vault_root = Path(settings.vault_path)
    vault_root.mkdir(parents=True, exist_ok=True)

    results = []
    all_extracted_tasks = []

    for f in files:
        original_filename = f.filename or "unnamed_file"
        try:
            # Sanitize filename and handle duplicates
            safe_filename = _sanitize_filename(original_filename)
            target_path = vault_root / safe_filename
            
            # Handle duplicate filenames by appending timestamp
            if target_path.exists():
                stem = target_path.stem
                suffix = target_path.suffix
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_filename = f"{stem}_{timestamp}{suffix}"
                target_path = vault_root / safe_filename
            
            # Save file to vault
            try:
                content = await f.read()
                if not content:
                    results.append(
                        {
                            "filename": original_filename,
                            "status": "error",
                            "error": "File is empty",
                        }
                    )
                    continue
                target_path.write_bytes(content)
            except Exception as exc:
                results.append(
                    {
                        "filename": original_filename,
                        "status": "error",
                        "error": f"Failed to save file: {str(exc)}",
                    }
                )
                continue

            # Process and index file
            try:
                chunk_count, extracted_tasks = await _process_and_index_file(target_path, original_filename, db)
                all_extracted_tasks.extend(extracted_tasks)
                
                results.append(
                    {
                        "filename": original_filename,
                        "status": "ingested",
                        "chunks_indexed": chunk_count,
                        "tasks_extracted": len(extracted_tasks),
                    }
                )
            except Exception as exc:
                # If processing fails, we still keep the raw file but report error
                error_msg = str(exc)
                # Make error message more user-friendly
                if "not installed" in error_msg.lower():
                    error_msg = "Required library not installed. Please install backend dependencies."
                elif "not found" in error_msg.lower():
                    error_msg = "File processing library not found. Please check backend setup."
                
                results.append(
                    {
                        "filename": original_filename,
                        "status": "error",
                        "error": error_msg,
                    }
                )
                continue
        except Exception as exc:
            # Catch-all for any unexpected errors
            results.append(
                {
                    "filename": original_filename,
                    "status": "error",
                    "error": f"Unexpected error: {str(exc)}",
                }
            )
            continue

    return {"results": results, "detected_tasks": all_extracted_tasks}


@router.post("/text")
async def ingest_text(text: str, source: str = "manual", db: Session = Depends(get_db)):
    """
    Manually ingest text content.

    The text is chunked, stored in the vector DB, and tasks are automatically extracted.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")

    chunks = chunk_text(text)
    store = VectorStore()

    metadatas = []
    ids = []
    for idx, chunk in enumerate(chunks):
        chunk_id = f"manual-{uuid.uuid4()}-{idx}"
        ids.append(chunk_id)
        metadatas.append(
            {
                "source": source,
                "chunk_index": idx,
            }
        )

    await run_in_threadpool(store.add_documents, chunks, metadatas, ids)

    # Extract tasks from text
    extracted_tasks = []
    try:
        task_resp = await generate(
            prompt=(
                "Extract actionable tasks from the following text.\n"
                "Return ONLY a JSON array of objects with keys:\n"
                '  - "title" (string, required)\n'
                '  - "description" (string, optional)\n'
                '  - "due_date" (string, optional)\n'
                '  - "priority" (string, optional)\n\n'
                f"Text:\n{text[:3000]}\n"
            )
        )
        tasks_json = _safe_extract_json_array(task_resp)

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
            extracted_tasks.append(
                {
                    "id": model.id,
                    "title": model.title,
                    "description": model.description,
                    "due_date": model.due_date,
                    "priority": model.priority,
                    "status": model.status,
                }
            )
    except Exception:
        pass

    return {"status": "ingested", "chunks_indexed": len(chunks), "detected_tasks": extracted_tasks}

