"""
Embedding model wrapper using sentence-transformers.

This module provides a thin abstraction over a local sentence-transformers
model so the rest of the codebase can generate embeddings without caring
about model details.
"""
from typing import List, Optional

import numpy as np

try:
    # Heavy import – done lazily in _get_model() as well, but this allows
    # fast failure if the dependency is completely missing.
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    SentenceTransformer = None  # type: ignore


_model: Optional["SentenceTransformer"] = None


def _get_model() -> "SentenceTransformer":
    """
    Get or lazily load the global embedding model instance.

    The concrete model name is aligned with `config/models.yaml` which
    defaults to `all-MiniLM-L6-v2`.
    """
    global _model

    if _model is not None:
        return _model

    if SentenceTransformer is None:
        raise RuntimeError(
            "sentence-transformers is not installed. "
            "Install optional AI dependencies with:\n"
            "  pip install -r backend/requirements-ai.txt"
        )

    # Default model – should match config/models.yaml embeddings.model
    model_name = "all-MiniLM-L6-v2"
    _model = SentenceTransformer(model_name)
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts.

    Args:
        texts: List of text strings

    Returns:
        Numpy array of embeddings of shape (len(texts), dim)
    """
    if not texts:
        return np.zeros((0, 0), dtype="float32")

    model = _get_model()
    # sentence-transformers already returns a numpy array
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype("float32")

