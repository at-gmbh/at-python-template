"""
AI Configuration Module

Manages environment variables and configuration for AI/LLM components.
Uses pydantic-settings for type-safe configuration management.

Best Practices 2026:
- Centralized configuration with validation
- Environment-based secrets management
- Type-safe with Pydantic v2
- No hardcoded credentials
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIConfig(BaseSettings):
    """
    AI/LLM Configuration with environment variable support.

    Load from .env file or environment variables.
    """

    # OpenAI Configuration
    openai_api_key: str = Field(
        default="",
        description="OpenAI API Key (required for OpenAI models)"
    )

    model_name: str = Field(
        default="gpt-4o",
        description="Default LLM model to use (e.g., gpt-4o, gpt-4o-mini)"
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Model temperature (0.0 = deterministic, 2.0 = very creative)"
    )

    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum tokens in response (None = model default)"
    )

    # RAG Configuration
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model for vector search"
    )

    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=4000,
        description="Document chunk size for RAG"
    )

    chunk_overlap: int = Field(
        default=200,
        ge=0,
        le=1000,
        description="Overlap between document chunks"
    )

    retrieval_k: int = Field(
        default=4,
        ge=1,
        le=20,
        description="Number of documents to retrieve in RAG"
    )

    # Vector Store Configuration
    vector_store_path: Path = Field(
        default=Path("./chroma_db"),
        description="Path to local vector database"
    )

    # Agent Configuration
    agent_max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum iterations for agent reasoning"
    )

    agent_verbose: bool = Field(
        default=True,
        description="Enable verbose logging for agent execution"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def validate_required_keys(self) -> None:
        """Validate that required API keys are present."""
        if not self.openai_api_key:
            logger.warning(
                "OPENAI_API_KEY not set. Set it in .env or environment variables."
            )
            raise ValueError(
                "OPENAI_API_KEY is required. "
                "Copy .env.example to .env and add your key."
            )

    def model_post_init(self, __context) -> None:
        """Post-initialization hook."""
        # Create vector store directory if it doesn't exist
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"AI Config loaded: model={self.model_name}, temperature={self.temperature}")


# Singleton instance
_config: Optional[AIConfig] = None


def get_ai_config() -> AIConfig:
    """
    Get or create AIConfig singleton instance.

    Loads configuration from .env file in project root.

    Returns:
        AIConfig: Validated configuration instance

    Raises:
        ValueError: If required API keys are missing
    """
    global _config

    if _config is None:
        # Load .env from project root
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            logger.debug(f"Loaded .env from {env_path}")
        else:
            logger.warning(f".env file not found at {env_path}")

        _config = AIConfig()
        _config.validate_required_keys()

    return _config


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = get_ai_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   Model: {config.model_name}")
        print(f"   Embedding: {config.embedding_model}")
        print(f"   Vector Store: {config.vector_store_path}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
