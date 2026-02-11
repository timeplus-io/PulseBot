"""Base embedding provider interface for PulseBot."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers.

    All embedding providers (OpenAI, Ollama, etc.) implement this interface
    to provide a consistent API for generating text embeddings.

    Example:
        >>> provider = OpenAIEmbeddingProvider(api_key="...")
        >>> embedding = await provider.embed("Hello world")
        >>> print(len(embedding))  # 1536 for text-embedding-3-small
    """

    provider_name: str = "base"
    model: str = ""
    dimensions: int = 0

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        pass

    def is_available(self) -> bool:
        """Check if the embedding provider is available.

        Returns:
            True if the provider can generate embeddings
        """
        return True
