# Environment variables (offline-only)

This repo intentionally avoids committing any `.env*` files. Create these locally:

## Backend: `backend/.env`

```ini
# Encryption (future SQLCipher integration)
DB_KEY=change-me

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# STT
STT_MODEL=base

# Logging
LOG_LEVEL=INFO
```

## Desktop: `desktop/.env`

```ini
VITE_API_URL=http://localhost:8000
```


