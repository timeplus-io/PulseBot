"""Local embedding provider using sentence-transformers (no external service needed)."""

from __future__ import annotations

import asyncio
from functools import lru_cache

from pulsebot.embeddings.base import EmbeddingProvider
from pulsebot.utils import get_logger

logger = get_logger(__name__)

DEFAULT_MODEL = "all-MiniLM-L6-v2"


@lru_cache(maxsize=4)
def _load_model(model_name: str):  # type: ignore[return]
    """Load and cache a SentenceTransformer model (process-wide singleton)."""
    from sentence_transformers import SentenceTransformer  # type: ignore[import]
    return SentenceTransformer(model_name)


class LocalEmbeddingProvider(EmbeddingProvider):
    """Embedding provider backed by sentence-transformers — runs fully local.

    Uses ``all-MiniLM-L6-v2`` by default (~100 MB, CPU-friendly, 384-dim).
    The model is downloaded on first use and cached in the HuggingFace cache
    directory (~/.cache/huggingface/hub).  No API key or external service required.

    Example:
        >>> provider = LocalEmbeddingProvider()
        >>> embedding = await provider.embed("Hello world")
        >>> print(len(embedding))  # 384
    """

    provider_name = "local"
    dimensions = 384  # all-MiniLM-L6-v2 default; updated after model load

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        # Load synchronously at init so dimensions are known immediately.
        # The model is cached process-wide, so subsequent instantiations are free.
        try:
            m = _load_model(model)
            self.dimensions = m.get_sentence_embedding_dimension() or 384
            logger.info(
                "Initialized local embedding provider: model=%s dimensions=%d",
                model,
                self.dimensions,
            )
        except Exception as exc:
            logger.warning("Could not pre-load local embedding model %s: %s", model, exc)

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text (runs in a thread pool)."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._encode_one, text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts (runs in a thread pool)."""
        if not texts:
            return []
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._encode_batch, texts)

    def _encode_one(self, text: str) -> list[float]:
        m = _load_model(self.model)
        return m.encode(text, convert_to_numpy=True).tolist()

    def _encode_batch(self, texts: list[str]) -> list[list[float]]:
        m = _load_model(self.model)
        return [v.tolist() for v in m.encode(texts, convert_to_numpy=True)]
