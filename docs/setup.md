# Setup Guide

## Prerequisites

1. **Node.js 18+** and npm/yarn
2. **Python 3.11+** and pip
3. **Ollama** installed locally ([download](https://ollama.ai))
4. **SQLCipher** libraries (for encrypted database)

## Installation Steps

### 1. Clone and Setup

```bash
cd cortexdesk
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Optional (enable AI features like embeddings + Chroma RAG):
# pip install -r requirements-ai.txt
#
# Optional (enable offline STT for live meetings):
# pip install -r requirements-stt.txt
```

### 3. Install Ollama Models

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3:8b
```

### 4. Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Desktop App Setup

```bash
cd desktop
npm install
```

### 6. Configuration

1. Create `backend/.env` and `desktop/.env` (see `docs/env.md`)
3. Review `config/app.yaml` and `config/models.yaml`

### 7. Initialize Database

```bash
cd backend
python -c "from app.storage.db import init_db; init_db()"
```

## Running the Application

### Start Backend

```bash
cd backend
python -m app.main
```

Or use the script:
```bash
# Windows PowerShell
.\scripts\start_backend.ps1

# Linux/Mac
./scripts/start_backend.sh
```

### Start Desktop App

```bash
cd desktop
npm run dev
```

Or use the script:
```bash
# Windows PowerShell
.\scripts\start_desktop.ps1

# Linux/Mac
./scripts/start_desktop.sh
```

## Verification

1. Backend should be running on `http://localhost:8000`
2. Desktop app should open automatically
3. Check backend health: `curl http://localhost:8000/health`

## Troubleshooting

### SQLCipher Issues
- Windows: Install SQLCipher from [here](https://www.sqlite.org/download.html)
- Linux: `sudo apt-get install libsqlcipher-dev`
- Mac: `brew install sqlcipher`

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check model is installed: `ollama list`

### Port Conflicts
- Change ports in `config/app.yaml` if 8000 or 5173 are in use

