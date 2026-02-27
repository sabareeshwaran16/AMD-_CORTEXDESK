"""
Database configuration and session management.
Uses SQLite locally. (SQLCipher integration is planned; kept offline-only.)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings, PROJECT_ROOT
from pathlib import Path

# Resolve DB path relative to repo root
db_path = (PROJECT_ROOT.parent / settings.db_path).resolve()
db_path.parent.mkdir(parents=True, exist_ok=True)

# Database URL (plain SQLite for now)
DATABASE_URL = f"sqlite:///{db_path.as_posix()}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Set to True for SQL debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

