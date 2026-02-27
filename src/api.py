from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import os
import sys
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.workspace_assistant import WorkspaceAssistant
from src.auth import AuthManager

assistant = None
auth_manager = AuthManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global assistant
    assistant = WorkspaceAssistant(data_dir="data")
    assistant.start()
    yield
    assistant.stop()

app = FastAPI(title="Local AI Workspace Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str

class TaskUpdate(BaseModel):
    task_id: int
    status: str

class SignupRequest(BaseModel):
    username: str
    password: str
    email: str

class LoginRequest(BaseModel):
    username: str
    password: str

def verify_auth(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.replace("Bearer ", "")
    session = auth_manager.verify_token(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return session

@app.get("/")
async def root():
    return {
        "name": "Local AI Workspace Assistant",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/auth/signup")
async def signup(req: SignupRequest):
    return auth_manager.signup(req.username, req.password, req.email)

@app.post("/auth/login")
async def login(req: LoginRequest):
    return auth_manager.login(req.username, req.password)

@app.post("/auth/logout")
async def logout(authorization: Optional[str] = Header(None)):
    if not authorization:
        return {"success": False, "error": "No token provided"}
    token = authorization.replace("Bearer ", "")
    return auth_manager.logout(token)

@app.get("/auth/verify")
async def verify(authorization: Optional[str] = Header(None)):
    session = verify_auth(authorization)
    return {"success": True, "user": session["username"]}

@app.get("/status")
async def get_status():
    return assistant.get_status()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    verify_auth(authorization)
    try:
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"[OK] File saved: {file_path}")
        
        # Check if image file for OCR
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']:
            print(f"[OK] Image detected, performing OCR...")
            try:
                from src.ocr import extract_text_from_image, is_ocr_available
                
                if is_ocr_available():
                    extracted_text = extract_text_from_image(file_path)
                    print(f"[OK] OCR extracted {len(extracted_text)} characters")
                    
                    text_file_path = file_path + ".txt"
                    with open(text_file_path, "w", encoding="utf-8") as f:
                        f.write(extracted_text)
                    
                    assistant.process_file(text_file_path)
                    
                    return {
                        "filename": file.filename,
                        "status": "processing",
                        "ocr": True,
                        "text_length": len(extracted_text)
                    }
                else:
                    return {"filename": file.filename, "status": "error", "message": "OCR not available. Install Tesseract."}
            except Exception as e:
                print(f"[ERROR] OCR failed: {str(e)}")
                return {"filename": file.filename, "status": "error", "message": f"OCR failed: {str(e)}"}
        
        assistant.process_file(file_path)
        print(f"[OK] File processing started")
        
        return {
            "filename": file.filename,
            "status": "processing",
            "path": file_path
        }
    except Exception as e:
        print(f"[ERROR] Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search(query: SearchQuery):
    try:
        # Check if vector DB has data
        if not assistant.vector_db.vectors:
            return {
                "query": query.query,
                "results": [],
                "count": 0,
                "message": "No documents indexed yet. Upload some documents first."
            }
        
        # Perform semantic search directly
        query_vector = assistant.embedding_model.encode(query.query)
        results = assistant.vector_db.search(query_vector, top_k=5)
        
        # Format results for display
        formatted_results = []
        for result in results:
            metadata = result.get("metadata", {})
            formatted_results.append({
                "text": metadata.get("text", "")[:500],  # First 500 chars
                "source": metadata.get("source", "Unknown"),
                "similarity": float(result.get("similarity", 0)),
                "timestamp": metadata.get("timestamp", "")
            })
        
        return {
            "query": query.query,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    except Exception as e:
        print(f"[ERROR] Search failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/tasks")
async def get_tasks():
    tasks = assistant.get_tasks()
    return {"tasks": tasks, "count": len(tasks)}

@app.get("/memory/recent")
async def get_recent_memory(days: int = 7):
    episodes = assistant.episodic_memory.query_recent(days=days)
    return {"episodes": episodes, "count": len(episodes)}

@app.post("/feedback/correction")
async def record_correction(original: str, corrected: str, correction_type: str):
    assistant.procedural_memory.record_correction(original, corrected, correction_type)
    return {"status": "recorded"}

@app.get("/confirmations")
async def get_confirmations():
    pending = assistant.get_pending_confirmations()
    return {"pending": pending, "count": len(pending)}

@app.post("/confirmations/{item_id}/approve")
async def approve_confirmation(item_id: str, edited_data: dict = None):
    approved = assistant.approve_item(item_id, edited_data)
    return {"status": "approved", "item": approved}

@app.post("/confirmations/{item_id}/reject")
async def reject_confirmation(item_id: str, reason: str = None):
    rejected = assistant.reject_item(item_id, reason)
    return {"status": "rejected", "item": rejected}

@app.get("/ai/status")
async def get_ai_status():
    """Get AI system status"""
    return assistant.get_ai_status()

@app.post("/conflicts/detect")
async def detect_conflicts():
    """Detect conflicts in tasks"""
    assistant.detect_conflicts()
    return {"status": "detecting"}

@app.delete("/tasks/{task_index}")
async def delete_task(task_index: int):
    """Delete a task by index"""
    tasks = assistant.get_tasks()
    if 0 <= task_index < len(tasks):
        deleted = assistant.task_agent.tasks.pop(task_index)
        return {"status": "deleted", "task": deleted}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/meetings")
async def get_meetings():
    """Get all processed meetings in structured format"""
    episodes = assistant.episodic_memory.query_recent(days=30, event_type="task")
    return {"meetings": episodes, "count": len(episodes)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
