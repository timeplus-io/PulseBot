"""OpenAI embedding provider for PulseBot."""

from __future__ import annotations

from typing import Any

from pulsebot.embeddings.base import EmbeddingProvider
from pulsebot.utils import get_logger

logger = get_logger(__name__)

# Model dimensions mapping
OPENAI_MODEL_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider.

    Uses OpenAI's embedding API to generate text embeddings.
    Supports text-embedding-3-small, text-embedding-3-large, and text-embedding-ada-002.

    Example:
        >>> provider = OpenAIEmbeddingProvider(api_key="sk-...")
        >>> embedding = await provider.embed("Hello world")
        >>> print(len(embedding))  # 1536

        >>> provider = OpenAIEmbeddingProvider(
        ...     api_key="sk-...",
        ...     model="text-embedding-3-large"
        ... )
        >>> embedding = await provider.embed("Hello world")
        >>> print(len(embedding))  # 3072
    """

    provider_name = "openai"

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int | None = None,
    ):
        """Initialize OpenAI embedding provider.

        Args:
            api_key: OpenAI API key
            model: Model name (text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002)
            dimensions: Optional explicit dimensions (auto-detected if not set)
        """
        self.api_key = api_key
        self.model = model
        self._client: Any = None

        # Auto-detect dimensions from model name
        if dimensions is None:
            self.dimensions = self._get_dimensions_for_model(model)
        else:
            self.dimensions = dimensions

        logger.info(f"Initialized OpenAI embedding provider: model={model}, dimensions={self.dimensions}")

    def _get_dimensions_for_model(self, model: str) -> int:
        """Get dimensions for a specific model.

        Args:
            model: Model name

        Returns:
            Embedding dimensions
        """
        return OPENAI_MODEL_DIMENSIONS.get(model, 1536)

    @property
    def client(self) -> Any:
        """Get or create OpenAI client (lazy initialization)."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
        return self._client

    def is_available(self) -> bool:
        """Check if the provider is available (has API key)."""
        return bool(self.api_key)

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            ValueError: If API key is not configured
            RuntimeError: If API request fails
        """
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embedding generation failed: {e}")
            raise RuntimeError(f"Failed to generate embedding: {e}")

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        if not texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts,
            )
            # Sort by index to maintain order
            embeddings = sorted(response.data, key=lambda x: x.index)
            return [e.embedding for e in embeddings]
        except Exception as e:
            logger.error(f"OpenAI batch embedding generation failed: {e}")
            raise RuntimeError(f"Failed to generate embeddings: {e}")
