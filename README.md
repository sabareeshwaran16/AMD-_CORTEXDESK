<<<<<<< HEAD
# Local AI Workspace Assistant

A fully local, privacy-first AI workspace assistant that runs 100% offline with no cloud calls.

## Features

- **100% Local Processing**: All AI operations run on your machine
- **Privacy-First**: No data leaves your computer
- **Multi-Agent Architecture**: Specialized agents for different tasks
- **Document Processing**: PDF, DOCX, XLSX, TXT support
- **Meeting Intelligence**: Extract action items, decisions, and summaries
- **Task Management**: Automatic task extraction and prioritization
- **Semantic Search**: RAG-based document search
- **Encrypted Storage**: All data encrypted at rest

## Architecture

### Agents
- **Document Agent**: Parses various file formats
- **Meeting Agent**: Extracts actions, decisions, and summaries
- **Task Agent**: Synthesizes and prioritizes tasks
- **Research Agent**: Semantic search with RAG
- **Supervisor Agent**: Orchestrates all agents

### Memory System
- **Working Memory**: Short-term in-memory cache
- **Episodic Memory**: Long-term event storage (SQLite)
- **Procedural Memory**: Learning from corrections
- **Semantic Memory**: Vector database for search

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy model (optional, for NER):
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Option 1: Web Interface

1. Start the API server:
```bash
python src/api.py
```

2. Open `src/ui/index.html` in your browser

### Option 2: CLI

```bash
python src/cli.py
```

### Option 3: Python API

```python
from src.core.workspace_assistant import WorkspaceAssistant

# Initialize
assistant = WorkspaceAssistant(data_dir="data")
assistant.start()

# Process a document
assistant.process_file("path/to/document.pdf")

# Search documents
assistant.search("project deadline")

# Get tasks
tasks = assistant.get_tasks()

# Stop
assistant.stop()
```

## API Endpoints

- `GET /` - System info
- `GET /status` - Agent status
- `POST /upload` - Upload document
- `POST /search` - Search documents
- `GET /tasks` - Get all tasks
- `GET /memory/recent` - Recent memory
- `POST /feedback/correction` - Record correction

## Project Structure

```
pro 1/
├── src/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── document_agent.py
│   │   ├── meeting_agent.py
│   │   ├── task_agent.py
│   │   ├── research_agent.py
│   │   └── supervisor_agent.py
│   ├── core/
│   │   ├── event_bus.py
│   │   ├── memory.py
│   │   └── workspace_assistant.py
│   ├── storage/
│   │   └── vector_db.py
│   ├── ui/
│   │   └── index.html
│   ├── api.py
│   └── cli.py
├── data/
│   ├── episodic.db
│   ├── procedural.db
│   ├── vectors.pkl
│   └── uploads/
├── config/
└── requirements.txt
```

## Security Features

- **Encryption at Rest**: All sensitive data encrypted using Fernet
- **No Network Calls**: Completely offline operation
- **Local Storage Only**: Data never leaves your machine
- **Access Control**: Agent-level memory permissions

## Extending the System

### Add a New Agent

```python
from src.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, event_bus, working_memory):
        super().__init__(
            agent_id="custom_agent",
            capabilities=["custom_capability"],
            event_bus=event_bus,
            working_memory=working_memory
        )
    
    def process(self, task):
        # Your logic here
        result = {"status": "completed"}
        self.publish_event("custom_event", result)
        return result
```

### Add Event Handler

```python
def on_custom_event(event):
    print(f"Custom event: {event}")

assistant.event_bus.subscribe("custom_event", on_custom_event)
```

## Performance Optimization

For production use, replace SimpleEmbedding with:

```python
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
```

Replace SimpleVectorDB with FAISS:

```python
import faiss

index = faiss.IndexFlatL2(384)
```

## Troubleshooting

**Issue**: Agents not processing tasks
- Check agent status: `assistant.get_status()`
- Verify event bus is running: `assistant.event_bus.running`

**Issue**: Out of memory
- Reduce vector DB size
- Clear working memory periodically
- Use smaller embedding models

**Issue**: Slow processing
- Process files in batches
- Use GPU acceleration for embeddings
- Optimize chunking strategy

## Roadmap

- [ ] Audio transcription with Whisper
- [ ] Calendar integration
- [ ] Knowledge graph visualization
- [ ] Multi-language support
- [ ] Model fine-tuning interface
- [ ] Conflict resolution UI
- [ ] Advanced analytics dashboard

## License

MIT License - Use freely for personal and commercial projects

## Privacy Statement

This system is designed for complete privacy:
- No telemetry or analytics
- No cloud API calls
- No data collection
- All processing happens locally
- You own and control all data

## Contributing

This is a minimal implementation. Contributions welcome for:
- Additional file format support
- Better NLP models
- UI improvements
- Performance optimizations
- Documentation

---

**Built with privacy in mind. Your data stays yours.**
=======
# CortexDesk

A local-first, privacy-focused desktop assistant that helps you manage tasks, notes, meetings, and research - all running 100% offline on your machine.

## Architecture

- **Desktop App**: Electron + React + TypeScript
- **Backend**: Python + FastAPI
- **AI Engine**: Local LLM (Ollama), offline STT (Whisper), RAG with Chroma
- **Storage**: SQLite + SQLCipher (encrypted), Chroma vector DB, encrypted file vault

## Features

- 📁 **Document Ingestion**: PDF, DOCX, XLSX, TXT
- 🎤 **Live Meeting Mode**: Offline speech-to-text and meeting summarization
- 📧 **Email/Chat Import**: Import exported emails (.pst, .mbox) and chats (WhatsApp, Slack)
- 🔍 **Research Copilot**: RAG-powered semantic search over your local documents
- ✅ **Task Management**: AI-extracted tasks with human-in-the-loop confirmation
- 📅 **Intelligent Scheduler**: Local calendar with conflict resolution
- 🧠 **Knowledge Graph**: Structured knowledge from your data
- 🔒 **100% Offline**: No cloud calls, all data stays local

## Setup

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Ollama installed locally (for LLM)
- SQLCipher libraries

### Installation

1. Install desktop dependencies:
```bash
cd desktop
npm install
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up local models (Ollama):
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3:8b  # or your preferred model
```

4. Configure paths in `config/app.yaml`

### Running

1. Start backend:
```bash
cd backend
python -m app.main
```

2. Start desktop app:
```bash
cd desktop
npm run dev
```

## Project Structure

```
cortexdesk/
├─ desktop/          # Electron + React + TS
├─ backend/          # Python + FastAPI
├─ config/           # Configuration files
├─ data/             # Local data (gitignored)
└─ docs/             # Documentation
```

## Security & Privacy

- All data encrypted at rest (SQLCipher + file vault encryption)
- No external network calls (except optional model downloads)
- Offline-by-default
- Permission-based access control

## License

[Your License Here]

>>>>>>> 4dea5a4cbc3df63cdf8c33784535c5395fb60160
