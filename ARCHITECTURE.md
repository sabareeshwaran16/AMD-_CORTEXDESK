# System Architecture Documentation

## Overview

The Local AI Workspace Assistant is a multi-agent system designed for privacy-first, offline AI processing.

## Architecture Layers

### 1. User Interaction Layer
- **Web UI** (`src/ui/index.html`): Browser-based interface
- **REST API** (`src/api.py`): FastAPI server
- **CLI** (`src/cli.py`): Command-line interface

### 2. Orchestration Layer
- **Supervisor Agent** (`src/agents/supervisor_agent.py`): Routes tasks to appropriate agents
- **Agent Registry** (`src/agents/base_agent.py`): Manages agent lifecycle and capabilities
- **Event Bus** (`src/core/event_bus.py`): Asynchronous inter-agent communication

### 3. Intelligence Layer (Agents)

#### Document Agent
- **Purpose**: Parse various file formats
- **Capabilities**: `parse_pdf`, `parse_docx`, `parse_xlsx`, `parse_txt`
- **Output**: Structured text with metadata

#### Meeting Agent
- **Purpose**: Extract insights from meeting notes
- **Capabilities**: `extract_actions`, `summarize`, `extract_decisions`
- **Output**: Action items, decisions, summaries with confidence scores

#### Task Agent
- **Purpose**: Synthesize and prioritize tasks
- **Capabilities**: `synthesize_tasks`, `deduplicate`, `prioritize`
- **Output**: Deduplicated, prioritized task list

#### Research Agent
- **Purpose**: Semantic search over documents
- **Capabilities**: `semantic_search`, `answer_query`
- **Output**: Relevant documents with similarity scores

### 4. Memory Layer

#### Working Memory
- **Type**: In-memory cache
- **Lifetime**: Configurable TTL (default 1 hour)
- **Use**: Short-term agent state

#### Episodic Memory
- **Type**: SQLite database
- **Lifetime**: Persistent (configurable retention)
- **Use**: Event history, completed tasks, meetings

#### Procedural Memory
- **Type**: SQLite database
- **Lifetime**: Persistent
- **Use**: User corrections, learned patterns

#### Semantic Memory
- **Type**: Vector database (pickle-based)
- **Lifetime**: Persistent
- **Use**: Document embeddings for RAG

### 5. Storage Layer
- **Vector DB** (`src/storage/vector_db.py`): Semantic search
- **Encrypted Storage** (`src/core/memory.py`): Fernet encryption
- **File System**: Local document storage

## Data Flow

```
User Upload → Document Agent → Text Extraction
                                      ↓
                              Meeting Agent → Action Extraction
                                      ↓
                               Task Agent → Deduplication & Prioritization
                                      ↓
                            Episodic Memory → Storage
                                      ↓
                             Research Agent → Indexing
                                      ↓
                              Vector DB → Semantic Search
```

## Event Flow

1. **Document Processed Event**
   - Triggered by: Document Agent
   - Subscribers: Research Agent, Meeting Agent
   - Payload: Extracted text, metadata

2. **Meeting Analyzed Event**
   - Triggered by: Meeting Agent
   - Subscribers: Task Agent
   - Payload: Actions, decisions, summary

3. **Tasks Synthesized Event**
   - Triggered by: Task Agent
   - Subscribers: UI, Episodic Memory
   - Payload: Task list with priorities

4. **Research Completed Event**
   - Triggered by: Research Agent
   - Subscribers: UI
   - Payload: Search results

## Agent Communication Protocol

### Message Format
```json
{
  "message_id": "agent_timestamp",
  "from_agent": "agent_id",
  "event_type": "event_name",
  "payload": {},
  "timestamp": "ISO8601"
}
```

### Task Format
```json
{
  "capability": "capability_name",
  "param1": "value1",
  "param2": "value2"
}
```

## Security Architecture

### Encryption
- **Algorithm**: Fernet (symmetric encryption)
- **Key Storage**: Local file system (`data/keys/`)
- **Scope**: Sensitive data at rest

### Access Control
- **Agent Isolation**: Each agent has separate working memory namespace
- **Permission Model**: Capability-based access
- **Audit Logging**: All memory access logged

### Privacy Guarantees
- **No Network Calls**: All processing local
- **No Telemetry**: Zero data collection
- **User Control**: Manual confirmation for critical actions

## Performance Characteristics

### Throughput
- **Document Processing**: ~1-2 seconds per page
- **Task Extraction**: ~0.5 seconds per document
- **Semantic Search**: ~0.1 seconds per query

### Scalability
- **Concurrent Agents**: 4 (configurable)
- **Max Document Size**: Limited by RAM
- **Vector DB Size**: ~1GB per 100K documents

### Resource Usage
- **RAM**: ~500MB baseline + document size
- **CPU**: Multi-threaded agent processing
- **Disk**: Depends on document corpus

## Extension Points

### Adding New Agents
1. Inherit from `BaseAgent`
2. Implement `process()` method
3. Register capabilities
4. Subscribe to relevant events

### Adding New File Formats
1. Add parser method to `DocumentAgent`
2. Update `file_type_map` in `WorkspaceAssistant`
3. Add to supported formats list

### Custom Memory Backends
1. Implement memory interface
2. Replace in `WorkspaceAssistant.__init__()`
3. Update configuration

## Failure Handling

### Agent Failures
- **Detection**: Status monitoring
- **Recovery**: Automatic restart (future)
- **Fallback**: Task re-queuing

### Data Corruption
- **Prevention**: Transactional updates
- **Detection**: Checksum validation
- **Recovery**: Backup restoration

### Resource Exhaustion
- **Prevention**: Queue limits, backpressure
- **Detection**: Resource monitoring
- **Recovery**: Graceful degradation

## Configuration

### System Config (`config/config.json`)
- Agent settings
- Memory parameters
- Security options
- Performance tuning

### Environment Variables
- `DATA_DIR`: Data storage location
- `LOG_LEVEL`: Logging verbosity
- `MAX_AGENTS`: Concurrent agent limit

## Monitoring

### Agent Status
- `idle`: Ready for tasks
- `processing`: Executing task
- `error`: Failed state

### Metrics
- Tasks processed
- Documents indexed
- Search queries
- Memory usage

## Future Enhancements

1. **Agent Health Monitoring**: Heartbeat checks, auto-restart
2. **Distributed Processing**: Multi-machine support
3. **Advanced NLP**: Fine-tuned models
4. **Knowledge Graph**: Entity relationship visualization
5. **Conflict Resolution**: Automated contradiction detection
6. **Incremental Updates**: Change-based processing
7. **Model Management**: Version control, A/B testing
