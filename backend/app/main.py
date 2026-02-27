"""
CortexDesk Backend - FastAPI Application
Main entry point for the backend API server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.storage.db import init_db

settings = get_settings()

app = FastAPI(
    title="CortexDesk API",
    description="Local-first AI assistant backend",
    version="1.0.0",
)

# Ensure DB tables exist on startup
@app.on_event("startup")
async def _startup():
    init_db()

# CORS middleware (only allow localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["http://localhost:5174"],  # Add common Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "CortexDesk API",
        "version": "1.0.0",
        "status": "online",
        "offline_mode": True,
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    """Health check endpoint accessible from frontend."""
    return {"status": "healthy", "version": "1.0.0"}

# Import and register routers
from app.api import ingest, meetings, research, tasks, scheduler, analytics

app.include_router(ingest.router, prefix="/api/ingest", tags=["ingestion"])
app.include_router(meetings.router, prefix="/api/meetings", tags=["meetings"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)

