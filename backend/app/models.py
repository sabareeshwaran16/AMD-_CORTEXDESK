"""
SQLAlchemy models for CortexDesk.

Kept intentionally minimal so the app can run locally without migrations.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.db import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # pending | detected | approved | rejected | done
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    priority: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Stored as ISO-ish string for simplicity (can be migrated to DateTime later)
    due_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    scheduled_for: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class MeetingModel(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str | None] = mapped_column(String(300), nullable=True)
    transcript: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

