"""
Local LLM client (Ollama).

All calls are made against a local Ollama server (default http://localhost:11434)
as configured in `config/models.yaml`. No cloud calls are performed.
"""
from typing import Optional, AsyncGenerator, Dict, Any, List

import yaml
from pathlib import Path

from fastapi.concurrency import run_in_threadpool

from app.security.network_guard import check_network_allowed

try:
    import ollama  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    ollama = None


def load_model_config() -> dict:
    """Load model configuration from models.yaml."""
    config_path = Path(__file__).parent.parent.parent.parent / "config" / "models.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
            return config.get("llm", {})
    return {}


def _build_messages(prompt: str, system_prompt: Optional[str]) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


async def generate(prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Generate text using local LLM (Ollama).

    This runs in a threadpool so it does not block the FastAPI event loop.
    """
    if ollama is None:
        raise RuntimeError(
            "ollama Python package is not installed. "
            "Install optional AI dependencies with:\n"
            "  pip install -r backend/requirements-ai.txt\n"
            "Also ensure the Ollama daemon is running locally."
        )

    cfg = load_model_config()
    base_url = cfg.get("base_url", "http://localhost:11434")
    model_name = cfg.get("model", "llama3:8b")
    temperature = float(cfg.get("temperature", 0.7))
    max_tokens = int(cfg.get("max_tokens", 2048))

    if not check_network_allowed(base_url):
        raise RuntimeError(
            f"External network call blocked for base_url={base_url}. "
            "Ollama must run locally (e.g., http://localhost:11434)."
        )

    messages = _build_messages(prompt, system_prompt)

    def _call() -> str:
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={"temperature": temperature, "num_predict": max_tokens},
        )
        return response["message"]["content"]

    return await run_in_threadpool(_call)


async def generate_streaming(
    prompt: str, system_prompt: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """
    Generate text with a streaming response from Ollama.
    """
    if ollama is None:
        raise RuntimeError(
            "ollama Python package is not installed. "
            "Install optional AI dependencies with:\n"
            "  pip install -r backend/requirements-ai.txt\n"
            "Also ensure the Ollama daemon is running locally."
        )

    cfg = load_model_config()
    base_url = cfg.get("base_url", "http://localhost:11434")
    model_name = cfg.get("model", "llama3:8b")
    temperature = float(cfg.get("temperature", 0.7))
    max_tokens = int(cfg.get("max_tokens", 2048))

    if not check_network_allowed(base_url):
        raise RuntimeError(
            f"External network call blocked for base_url={base_url}. "
            "Ollama must run locally (e.g., http://localhost:11434)."
        )

    messages = _build_messages(prompt, system_prompt)

    def _iter():
        return ollama.chat(
            model=model_name,
            messages=messages,
            options={"temperature": temperature, "num_predict": max_tokens},
            stream=True,
        )

    # Run generator in a thread and yield chunks asynchronously
    iterator = await run_in_threadpool(_iter)
    for chunk in iterator:
        content = chunk.get("message", {}).get("content")
        if content:
            yield content

