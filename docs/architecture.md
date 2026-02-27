# CortexDesk Architecture

## Overview

CortexDesk is a local-first desktop assistant that processes your documents, meetings, and tasks entirely offline.

## Architecture Layers

### 1. User Interaction Layer (Desktop App)
- **Technology**: Electron + React + TypeScript
- **Location**: `desktop/`
- **Components**:
  - Dashboard
  - Meetings (Live Meeting Mode)
  - Research Workspace
  - Tasks
  - Settings

### 2. Local Input & Connector Layer
- **Technology**: Python
- **Location**: `backend/app/connectors/`
- **Components**:
  - File readers (PDF, DOCX, XLSX, TXT)
  - Folder watcher
  - Mic listener (offline STT)
  - Mail reader (.pst, .mbox)
  - Chat reader (WhatsApp, Slack)

### 3. Local Preprocessing Engine
- **Technology**: Python (spaCy, dateparser, custom)
- **Location**: `backend/app/preprocessing/`
- **Components**:
  - Text cleaning
  - Language detection
  - Speaker diarization
  - NER
  - Deadline normalization
  - Chunking

### 4. Local AI Intelligence Core
- **Technology**: Python (Ollama, sentence-transformers, Chroma)
- **Location**: `backend/app/ai/`
- **Components**:
  - RAG engine
  - Meeting summarizer
  - Action item extractor
  - Decision tracker
  - Risk detector

### 5. Human-in-the-Loop Confirmation Layer
- **Technology**: React (UI) + Python (API)
- **Location**: `desktop/src/components/ManualConfirmationPanel/` + `backend/app/api/tasks.py`
- **Flow**: AI proposes → User approves/rejects/edits → Task created

### 6. Intelligent Scheduler
- **Technology**: Python
- **Location**: `backend/app/scheduler/`
- **Components**:
  - Schedule engine
  - Conflict resolver
  - Priority inference
  - Reminder system

### 7. Knowledge Structuring Layer
- **Technology**: Python + SQLite
- **Location**: `backend/app/knowledge/`
- **Components**:
  - Task graph
  - Decision log
  - Notes graph
  - Project memory

### 8. Local Storage
- **Technology**: SQLite + SQLCipher, Chroma, encrypted file vault
- **Location**: `backend/app/storage/`, `data/`
- **Components**:
  - Encrypted SQL database
  - Vector DB (Chroma)
  - File vault

### 9. Retrieval & Analytics
- **Technology**: Python + React
- **Location**: `backend/app/retrieval/`, `desktop/src/pages/`
- **Components**:
  - Semantic search
  - Knowledge explorer
  - Task board
  - Productivity insights

### 10. Security & Privacy Core (Cross-cutting)
- **Technology**: Python middleware + Electron security
- **Location**: `backend/app/security/`
- **Components**:
  - Network guard (blocks external calls)
  - Permissions manager
  - Audit logging
  - Encryption

### 11. Feedback & Learning (Cross-cutting)
- **Technology**: Python
- **Location**: `backend/app/feedback/`
- **Components**:
  - User corrections tracking
  - Personalization
  - Prompt tuning

## Data Flow

1. User drops file / starts meeting → **Connectors** ingest
2. **Preprocessing** cleans and chunks
3. **AI Core** extracts insights (tasks, summaries, etc.)
4. **Human-in-the-Loop** shows proposals → User approves
5. **Scheduler** proposes schedule → User confirms
6. **Knowledge Graph** structures data
7. **Storage** persists encrypted
8. **Retrieval** enables search and analytics

## Security Model

- **100% Offline**: No cloud calls (except optional model downloads)
- **Encryption**: SQLCipher for DB, AES-GCM for files
- **Permissions**: Explicit user consent for data access
- **Audit Logging**: All actions logged locally

