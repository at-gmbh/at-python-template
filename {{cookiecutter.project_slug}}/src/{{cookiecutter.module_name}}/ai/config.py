"""
AI Configuration Module

🎯 PHILOSOPHY: "Launchpad, not a prison"

This config provides sensible defaults via pydantic-settings, but you can
ALWAYS override them programmatically. Think of this as a starting point,
not a restriction.

Usage:
    # Use defaults from .env
    config = get_ai_config()

    # Override at runtime for experiments
    config.temperature = 0.9
    config.model_name = "gpt-4o-mini"

    # Or create custom configs
    custom_config = AIConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.0  # Deterministic
    )

Best Practices 2026:
- Environment variables for secrets (API keys)
- Code for experiments (model params)
- Version control for stable configs
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
    AI/LLM Configuration with flexible overrides.

    🚀 CUSTOMIZATION: All fields are mutable after creation.
    Change anything you need during development!

    Example:
        config = AIConfig()
        config.temperature = 1.2  # Experiment with creativity
        config.max_tokens = 2000  # Longer responses
    """

    # === OpenAI Configuration ===
    openai_api_key: str = Field(
        default="",
        description="OpenAI API Key (set via OPENAI_API_KEY env var)"
    )

    model_name: str = Field(
        default="gpt-4o",
        description="Default LLM model (gpt-4o, gpt-4o-mini, gpt-4-turbo)"
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

    # === Embedding Configuration (for RAG) ===
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model for vector search"
    )

    # === RAG Configuration ===
    # TODO: Customize these based on your document types
    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=4000,
        description="Document chunk size (adjust for your content)"
    )

    chunk_overlap: int = Field(
        default=200,
        ge=0,
        le=1000,
        description="Overlap between chunks (helps preserve context)"
    )

    retrieval_k: int = Field(
        default=4,
        ge=1,
        le=20,
        description="Number of documents to retrieve (more = more context, slower)"
    )

    # === Vector Store ===
    vector_store_path: Path = Field(
        default=Path("./chroma_db"),
        description="Local vector database path"
    )

    # === Agent Configuration ===
    agent_max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum agent reasoning steps"
    )

    agent_verbose: bool = Field(
        default=True,
        description="Enable verbose agent logging"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        # Allow mutation for easy experimentation
        frozen=False
    )

    def validate_required_keys(self) -> None:
        """
        Validate that required API keys are present.

        🎯 TIP: Skip this in unit tests by mocking get_ai_config()
        """
        if not self.openai_api_key:
            logger.warning(
                "OPENAI_API_KEY not set. Set it in .env or environment variables."
            )
            raise ValueError(
                "OPENAI_API_KEY is required. "
                "Copy .env.example to .env and add your key."
            )

    def model_post_init(self, __context) -> None:
        """Post-initialization: Create directories, log config."""
        # Create vector store directory if it doesn't exist
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"AI Config loaded: model={self.model_name}, "
            f"temp={self.temperature}, k={self.retrieval_k}"
        )


# === Singleton Pattern (Optional - Use if you want global config) ===
_config: Optional[AIConfig] = None


def get_ai_config(force_reload: bool = False) -> AIConfig:
    """
    Get or create AIConfig singleton instance.

    🎯 CUSTOMIZATION TIP: Don't like singletons? Just use AIConfig() directly!

    Args:
        force_reload: Reload config from environment (useful for testing)

    Returns:
        AIConfig: Validated configuration instance

    Raises:
        ValueError: If required API keys are missing

    Example:
        # Standard usage
        config = get_ai_config()

        # Force reload for testing
        config = get_ai_config(force_reload=True)

        # Or skip singleton entirely
        config = AIConfig(model_name="gpt-3.5-turbo")
    """
    global _config

    if _config is None or force_reload:
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


# === Helper: Reset Config (useful for testing) ===
def reset_config():
    """Reset singleton config. Useful for testing different configurations."""
    global _config
    _config = None


if __name__ == "__main__":
    # Demo: Test configuration loading
    try:
        config = get_ai_config()
        print("✅ Configuration loaded successfully")
        print(f"   Model: {config.model_name}")
        print(f"   Temperature: {config.temperature}")
        print(f"   Embedding: {config.embedding_model}")
        print(f"   Vector Store: {config.vector_store_path}")

        # Demo: Runtime override
        print("\n🔧 Overriding temperature...")
        config.temperature = 1.5
        print(f"   New temperature: {config.temperature}")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Quick fix:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OPENAI_API_KEY=sk-...")
