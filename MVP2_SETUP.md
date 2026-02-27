# MVP 2 - Ollama Integration Setup

## Prerequisites

### 1. Install Ollama

**Windows:**
```bash
# Download from https://ollama.ai/download
# Run the installer
```

**Verify Installation:**
```bash
ollama --version
```

### 2. Pull a Model

```bash
# Recommended: Llama 2 (7B - good balance)
ollama pull llama2

# Or smaller/faster:
ollama pull llama2:7b-chat

# Or larger/better:
ollama pull llama2:13b
```

### 3. Start Ollama Server

```bash
ollama serve
```

Keep this running in a separate terminal.

## Install Python Dependencies

```bash
pip install requests
```

## Features Added in MVP 2

### 1. AI-Powered Task Extraction
- Understands natural language
- No keywords required
- Extracts from any text

### 2. Meeting Summarization
- AI-generated summaries
- Key points extraction
- Decision tracking

### 3. Conflict Detection
- Duplicate task detection
- Deadline conflicts
- Missing information alerts

### 4. Fallback Mode
- If Ollama unavailable, falls back to rule-based
- System continues working without AI

## Testing

1. Start Ollama: `ollama serve`
2. Start API: `python src/api.py`
3. Upload text without keywords - AI will extract tasks
4. Check Meetings page for AI summaries

## Configuration

Edit `src/ai_core/ollama/client.py` to change:
- Model: `model="llama2"` (line 8)
- Temperature: `temperature=0.7` (line 13)
- Base URL: `base_url="http://localhost:11434"` (line 7)

## Troubleshooting

**Ollama not found:**
- Check if `ollama serve` is running
- Verify port 11434 is open
- System falls back to rule-based extraction

**Slow responses:**
- Use smaller model: `ollama pull llama2:7b-chat`
- Reduce temperature
- Use GPU if available

**Out of memory:**
- Use smaller model
- Close other applications
- Increase system RAM

## Next Steps

MVP 2 is ready! The system now uses AI when available, with automatic fallback to rule-based extraction.
