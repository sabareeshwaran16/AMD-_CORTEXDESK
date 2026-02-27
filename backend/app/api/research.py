"""
Research workspace endpoints.
RAG-powered semantic search over local documents.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.rag_engine import search_documents, answer_question

router = APIRouter()


class ResearchQuery(BaseModel):
    query: str
    max_results: int = 5


@router.post("/query")
async def research_query(query: ResearchQuery):
    """
    Perform semantic search over local documents using RAG.

    Returns only document chunks and metadata (no generated answer).
    """
    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = await search_documents(query.query, limit=query.max_results)
    return {
        "query": query.query,
        "results": results,
    }


class QuestionRequest(BaseModel):
    query: str
    context_limit: int = 5


@router.post("/question")
async def research_question(body: QuestionRequest):
    """
    Answer a question using RAG (LLM + retrieved context).

    Returns:
    - `answer`: model-generated answer
    - `citations`: list of document chunks used as context
    """
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = await answer_question(body.query, context_limit=body.context_limit)
    return result

