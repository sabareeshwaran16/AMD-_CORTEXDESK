import os
from src.core.event_bus import EventBus
from src.core.memory import WorkingMemory, EpisodicMemory, ProceduralMemory, EncryptedStorage
from src.agents.base_agent import AgentRegistry
from src.agents.document_agent import DocumentAgent
from src.agents.ai_meeting_agent import AIMeetingAgent
from src.agents.task_agent import TaskAgent
from src.agents.research_agent import ResearchAgent
from src.agents.supervisor_agent import SupervisorAgent
from src.agents.conflict_detector_agent import ConflictDetectorAgent
from src.storage.vector_db import SimpleVectorDB, SimpleEmbedding
from src.human_layer.confirmation import ConfirmationPanel
from src.ai_core.ollama.client import OllamaClient

class WorkspaceAssistant:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize core components
        self.event_bus = EventBus()
        self.working_memory = WorkingMemory()
        self.episodic_memory = EpisodicMemory(f"{data_dir}/episodic.db")
        self.procedural_memory = ProceduralMemory(f"{data_dir}/procedural.db")
        self.encrypted_storage = EncryptedStorage(f"{data_dir}/keys/encryption.key")
        
        # Initialize vector database
        self.vector_db = SimpleVectorDB(f"{data_dir}/vectors.pkl")
        self.embedding_model = SimpleEmbedding()
        
        # Initialize confirmation panel
        self.confirmation_panel = ConfirmationPanel(f"{data_dir}/confirmations.json")
        self.confirmation_panel._load()
        
        # Initialize Ollama (MVP 2)
        self.ollama = OllamaClient()
        self.ai_enabled = self.ollama.is_available()
        if self.ai_enabled:
            print("[OK] Ollama detected - AI-powered processing enabled")
        else:
            print("[WARN] Ollama not available - using rule-based processing")
        
        # Initialize agent registry
        self.registry = AgentRegistry()
        
        # Create agents
        self.document_agent = DocumentAgent(self.event_bus, self.working_memory)
        self.meeting_agent = AIMeetingAgent(
            self.event_bus, 
            self.working_memory, 
            self.confirmation_panel,
            use_ai=self.ai_enabled
        )
        self.task_agent = TaskAgent(self.event_bus, self.working_memory, self.episodic_memory)
        self.research_agent = ResearchAgent(
            self.event_bus, self.working_memory, 
            self.vector_db, self.embedding_model
        )
        self.conflict_detector = ConflictDetectorAgent(
            self.event_bus, self.working_memory, self.ollama if self.ai_enabled else None
        )
        
        # Register agents
        self.registry.register(self.document_agent)
        self.registry.register(self.meeting_agent)
        self.registry.register(self.task_agent)
        self.registry.register(self.research_agent)
        self.registry.register(self.conflict_detector)
        
        # Create supervisor
        self.supervisor = SupervisorAgent(self.registry, self.event_bus)
        
        # Setup event subscriptions
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        self.event_bus.subscribe("document_processed", self._on_document_processed)
        self.event_bus.subscribe("meeting_analyzed", self._on_meeting_analyzed)
        self.event_bus.subscribe("tasks_synthesized", self._on_tasks_synthesized)
    
    def _on_document_processed(self, event):
        print(f"[WorkspaceAssistant] Document processed event received")
        payload = event["payload"]
        text = payload.get("text", "")
        print(f"[WorkspaceAssistant] Text length: {len(text)} chars")
        
        # Chunk text for better search (500 char chunks with 100 char overlap)
        chunks = self._chunk_text(text, chunk_size=500, overlap=100)
        print(f"[WorkspaceAssistant] Created {len(chunks)} chunks for indexing")
        
        # Index each chunk
        for i, chunk in enumerate(chunks):
            self.research_agent.index_document(chunk, {
                "source": payload.get("file_path", ""),
                "timestamp": event["timestamp"],
                "chunk_id": i,
                "total_chunks": len(chunks)
            })
        
        # Analyze for meeting content
        print(f"[WorkspaceAssistant] Routing to meeting agent for extraction")
        self.supervisor.route_task({
            "capability": "extract_actions",
            "text": text,
            "source": payload.get("file_path", "")
        })
        print(f"[WorkspaceAssistant] Task routed to supervisor")
    
    def _chunk_text(self, text, chunk_size=500, overlap=100):
        """Split text into overlapping chunks for better search"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                if break_point > chunk_size * 0.5:  # At least 50% of chunk
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap  # Overlap for context
        
        return chunks
    
    def _on_meeting_analyzed(self, event):
        payload = event["payload"]
        actions = payload.get("actions", [])
        
        print(f"[WorkspaceAssistant] Meeting analyzed: {len(actions)} actions extracted")
        print(f"[WorkspaceAssistant] Actions are in confirmation panel, waiting for human approval")
        
        # Don't synthesize tasks - they're already in confirmation panel
        # Tasks will be added to task_agent only after approval
    
    def _on_tasks_synthesized(self, event):
        print(f"Tasks synthesized: {event['payload']['count']} tasks")
        
        # Run conflict detection
        tasks = event['payload'].get('tasks', [])
        if tasks:
            self.supervisor.route_task({
                "capability": "detect_conflicts",
                "tasks": tasks
            })
    
    def start(self):
        print("Starting Workspace Assistant...")
        self.event_bus.start()
        self.supervisor.start()
        print("System ready!")
    
    def stop(self):
        print("Stopping Workspace Assistant...")
        self.supervisor.stop()
        self.event_bus.stop()
        self.vector_db.save()
        print("System stopped.")
    
    def process_file(self, file_path: str):
        print(f"[WorkspaceAssistant] Processing file: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()
        file_type_map = {
            ".pdf": "pdf",
            ".docx": "docx",
            ".xlsx": "xlsx",
            ".txt": "txt",
            ".pptx": "pptx"
        }
        
        file_type = file_type_map.get(ext)
        if not file_type:
            print(f"Unsupported file type: {ext}")
            return
        
        print(f"[WorkspaceAssistant] Routing to document agent: parse_{file_type}")
        self.supervisor.route_task({
            "capability": f"parse_{file_type}",
            "file_path": file_path,
            "file_type": file_type
        })
    
    def search(self, query: str):
        self.supervisor.route_task({
            "capability": "semantic_search",
            "query": query
        })
    
    def get_tasks(self):
        return self.task_agent.get_all_tasks()
    
    def get_status(self):
        return self.supervisor.get_agent_status()
    
    def get_pending_confirmations(self):
        return self.confirmation_panel.get_pending()
    
    def approve_item(self, item_id, edited_data=None):
        approved = self.confirmation_panel.approve(item_id, edited_data)
        # Add approved task to task agent
        if approved["type"] == "task":
            self.task_agent.tasks.append(approved["data"])
        return approved
    
    def reject_item(self, item_id, reason=None):
        return self.confirmation_panel.reject(item_id, reason)
    
    def detect_conflicts(self):
        """Detect conflicts in current tasks"""
        tasks = self.get_tasks()
        self.supervisor.route_task({
            "capability": "detect_conflicts",
            "tasks": tasks
        })
    
    def get_ai_status(self):
        """Check if AI is enabled"""
        return {
            "ai_enabled": self.ai_enabled,
            "ollama_available": self.ollama.is_available() if self.ollama else False,
            "model": self.ollama.model if self.ollama else None
        }
