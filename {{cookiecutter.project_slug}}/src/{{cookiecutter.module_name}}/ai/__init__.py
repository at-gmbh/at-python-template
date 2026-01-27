"""
AI Starter Kit Module

This module provides ready-to-use AI components including:
- RAG (Retrieval-Augmented Generation) pipeline
- LangChain agents with tools
- Configuration management for LLM providers
- Structured prompts and logging

Best Practices (2026):
- Use structured outputs with Pydantic v2
- Environment-based configuration with pydantic-settings
- Modular prompt management
- Vector stores for efficient retrieval
- Observability with loguru
"""

from .config import AIConfig, get_ai_config
from .prompts import SystemPrompts

__all__ = [
    "AIConfig",
    "get_ai_config",
    "SystemPrompts",
]
