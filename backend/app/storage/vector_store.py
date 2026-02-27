"""
Vector store wrapper around Chroma.

This provides a minimal persistence-backed vector store used by the RAG engine.
All data stays on disk under `settings.vector_db_path`.
"""
from typing import List, Dict, Optional

from pathlib import Path

from app.core.config import settings
from app.ai.embeddings import embed_texts

try:
    import chromadb  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    chromadb = None


class VectorStore:
    """Chroma vector store wrapper."""

    def __init__(self, collection_name: str = "cortexdesk_documents"):
        if chromadb is None:
            raise RuntimeError(
                "chromadb is not installed. "
                "Install optional AI dependencies with:\n"
                "  pip install -r backend/requirements-ai.txt"
            )

        base_path = Path(settings.vector_db_path)
        base_path.mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(path=str(base_path))
        self._collection = self._client.get_or_create_collection(collection_name)

    def add_documents(self, texts: List[str], metadatas: List[Dict], ids: List[str]):
        """
        Add documents (already-chunked text) to the vector store.

        `metadatas` and `ids` must be the same length as `texts`.
        """
        if not texts:
            return

        if not (len(texts) == len(metadatas) == len(ids)):
            raise ValueError("texts, metadatas, and ids must have the same length")

        embeddings = embed_texts(texts)
        # chroma expects python lists, not numpy arrays
        self._collection.add(
            ids=ids,
            metadatas=metadatas,
            documents=texts,
            embeddings=embeddings.tolist(),
        )

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for documents similar to the query string.

        Returns a list of dicts with `text`, `score`, and `metadata`.
        """
        if not query:
            return []

        query_emb = embed_texts([query])
        results = self._collection.query(
            query_embeddings=query_emb.tolist(),
            n_results=limit,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        out: List[Dict] = []
        for text, meta, dist in zip(documents, metadatas, distances):
            out.append(
                {
                    "text": text,
                    "metadata": meta or {},
                    "score": float(dist),
                }
            )
        return out

