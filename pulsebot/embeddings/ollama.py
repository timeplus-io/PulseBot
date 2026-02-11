"""Ollama embedding provider for PulseBot."""

from __future__ import annotations

from typing import Any

import aiohttp

from pulsebot.embeddings.base import EmbeddingProvider
from pulsebot.utils import get_logger

logger = get_logger(__name__)

# Known Ollama embedding model dimensions
# These are common values, but actual dimensions may vary
OLLAMA_MODEL_DIMENSIONS = {
    "mxbai-embed-large": 1024,
    "all-minilm": 384,
    "all-minilm-l6-v2": 384,
    "nomic-embed-text": 768,
    "snowflake-arctic-embed": 1024,
    "bge-large": 1024,
    "bge-base": 768,
    "bge-small": 384,
}


class OllamaEmbeddingProvider(EmbeddingProvider):
    """Ollama embedding provider for local embedding models.

    Uses Ollama's /api/embeddings endpoint to generate text embeddings.
    Supports models like mxbai-embed-large, all-minilm, nomic-embed-text, etc.

    Example:
        >>> provider = OllamaEmbeddingProvider(
        ...     host="http://localhost:11434",
        ...     model="mxbai-embed-large"
        ... )
        >>> embedding = await provider.embed("Hello world")
        >>> print(len(embedding))  # 1024

        >>> provider = OllamaEmbeddingProvider(
        ...     host="http://localhost:11434",
        ...     model="all-minilm"
        ... )
        >>> embedding = await provider.embed("Hello world")
        >>> print(len(embedding))  # 384
    """

    provider_name = "ollama"

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "nomic-embed-text",
        dimensions: int | None = None,
        timeout_seconds: int = 30,
    ):
        """Initialize Ollama embedding provider.

        Args:
            host: Ollama server URL
            model: Model name (e.g., 'mxbai-embed-large', 'all-minilm', 'nomic-embed-text')
            dimensions: Optional explicit dimensions (auto-detected if not set)
            timeout_seconds: Request timeout
        """
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        self._dimensions: int | None = dimensions
        self._detected_dimensions: bool = False

        # If dimensions provided, use them; otherwise will auto-detect on first use
        if dimensions is not None:
            self.dimensions = dimensions
            self._detected_dimensions = True
            logger.info(f"Initialized Ollama embedding provider: host={host}, model={model}, dimensions={dimensions} (explicit)")
        else:
            # Try to get from known models, otherwise will auto-detect
            self.dimensions = self._get_dimensions_for_model(model)
            if self.dimensions > 0:
                self._detected_dimensions = True
                logger.info(f"Initialized Ollama embedding provider: host={host}, model={model}, dimensions={self.dimensions} (known)")
            else:
                logger.info(f"Initialized Ollama embedding provider: host={host}, model={model}, dimensions=auto-detect")

    def _get_dimensions_for_model(self, model: str) -> int:
        """Get known dimensions for a specific model.

        Args:
            model: Model name

        Returns:
            Embedding dimensions or 0 if unknown
        """
        # Check exact match
        if model in OLLAMA_MODEL_DIMENSIONS:
            return OLLAMA_MODEL_DIMENSIONS[model]

        # Check prefix match
        for known_model, dims in OLLAMA_MODEL_DIMENSIONS.items():
            if model.startswith(known_model) or known_model.startswith(model):
                return dims

        return 0

    async def _detect_dimensions(self) -> int:
        """Auto-detect embedding dimensions by calling the model.

        Returns:
            Detected dimensions

        Raises:
            RuntimeError: If detection fails
        """
        logger.debug(f"Auto-detecting dimensions for model: {self.model}")

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                payload = {
                    "model": self.model,
                    "prompt": "test",
                }

                async with session.post(
                    f"{self.host}/api/embeddings",
                    json=payload,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"Ollama API error: HTTP {response.status} - {error_text}")

                    data = await response.json()
                    embedding = data.get("embedding", [])
                    dimensions = len(embedding)

                    if dimensions == 0:
                        raise RuntimeError("Empty embedding returned")

                    logger.info(f"Detected dimensions for {self.model}: {dimensions}")
                    return dimensions

        except aiohttp.ClientError as e:
            raise RuntimeError(f"Failed to connect to Ollama at {self.host}: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to detect dimensions: {e}")

    async def _ensure_dimensions(self) -> None:
        """Ensure dimensions are detected if not already known."""
        if not self._detected_dimensions:
            self.dimensions = await self._detect_dimensions()
            self._detected_dimensions = True

    def is_available(self) -> bool:
        """Check if the provider is available.

        Note: This is a basic check. The actual availability
        is verified on first embed() call.
        """
        return True

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            RuntimeError: If embedding generation fails
        """
        # Ensure dimensions are detected
        await self._ensure_dimensions()

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                payload = {
                    "model": self.model,
                    "prompt": text,
                }

                async with session.post(
                    f"{self.host}/api/embeddings",
                    json=payload,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"Ollama API error: HTTP {response.status} - {error_text}")

                    data = await response.json()
                    embedding = data.get("embedding", [])

                    if not embedding:
                        raise RuntimeError("Empty embedding returned")

                    return embedding

        except aiohttp.ClientError as e:
            logger.error(f"Ollama connection error: {e}")
            raise RuntimeError(f"Failed to connect to Ollama at {self.host}: {e}")
        except Exception as e:
            logger.error(f"Ollama embedding generation failed: {e}")
            raise RuntimeError(f"Failed to generate embedding: {e}")

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Ollama doesn't support batch embedding natively, so we
        make individual requests and aggregate results.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        embeddings = []
        for text in texts:
            embedding = await self.embed(text)
            embeddings.append(embedding)

        return embeddings
