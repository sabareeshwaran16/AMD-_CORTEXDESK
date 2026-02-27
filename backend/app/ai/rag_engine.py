"""
RAG (Retrieval-Augmented Generation) engine.

Provides:
- `search_documents` for semantic search over local documents.
- `answer_question` for question answering with citations using local LLM.
"""
from typing import List, Dict, Any

from app.ai.llm_client import generate
from app.storage.vector_store import VectorStore


async def search_documents(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Perform semantic search over documents.

    Args:
        query: Search query
        limit: Maximum number of results

    Returns:
        List of relevant document chunks with metadata
    """
    store = VectorStore()
    results = store.search(query=query, limit=limit)
    return results


async def answer_question(query: str, context_limit: int = 5) -> Dict[str, Any]:
    """
    Answer a question using RAG.

    Args:
        query: User question
        context_limit: Number of document chunks to use as context

    Returns:
        Dict with `answer` and `citations` (list of chunks/metadata)
    """
    # 1. Retrieve relevant document chunks
    search_results = await search_documents(query, limit=context_limit)

    if not search_results:
        # Fallback: let LLM answer without context, but make it clear
        answer_text = await generate(
            prompt=(
                "User question:\n"
                f"{query}\n\n"
                "No relevant documents were found in the local knowledge base. "
                "Answer as best as you can, but mention that you couldn't find "
                "supporting local documents."
            )
        )
        return {"answer": answer_text, "citations": []}

    # 2. Build context from top documents
    context_snippets = []
    for idx, item in enumerate(search_results, start=1):
        meta = item.get("metadata", {}) or {}
        source = meta.get("source", "unknown")
        page = meta.get("page")
        header = f"[{idx}] source={source}"
        if page is not None:
            header += f", page={page}"
        header += ":\n"
        context_snippets.append(header + item.get("text", ""))

    context = "\n\n".join(context_snippets)

    # 3. Ask LLM with context
    prompt = (
        "You are a local research assistant. Answer the user's question using "
        "ONLY the provided context from local documents. If the context is "
        "insufficient, say so explicitly.\n\n"
        "Context:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{query}\n\n"
        "Answer (be concise, and refer to citations like [1], [2] where relevant):"
    )

    answer_text = await generate(prompt=prompt)

    return {
        "answer": answer_text,
        "citations": search_results,
    }

