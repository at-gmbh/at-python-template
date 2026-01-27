# AI Starter Kit

This module provides production-ready AI/LLM components based on LangChain and best practices from 2026.

## Features

### 🤖 RAG Pipeline (`rag.py`)
Retrieval-Augmented Generation for question answering over documents:
- Document loading (text, PDF)
- Intelligent chunking
- Vector embeddings with OpenAI
- ChromaDB for local storage
- Semantic search and retrieval
- Source attribution

### 🛠️ AI Agents (`agent.py`)
LangChain agents with tool-calling capabilities:
- Multiple pre-built tools (calculator, search, date)
- OpenAI function calling
- Structured inputs with Pydantic
- Multi-step reasoning
- Easy tool extension

### ⚙️ Configuration (`config.py`)
Type-safe configuration management:
- Environment-based secrets (`.env`)
- Pydantic validation
- Sensible defaults
- No hardcoded credentials

### 📝 Prompt Management (`prompts.py`)
Centralized prompt storage:
- System prompts for different tasks
- Versioned and reusable templates
- Easy A/B testing

## Quick Start

### 1. Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-proj-your-key-here
```

### 2. RAG Example

```python
from {{ cookiecutter.module_name }}.ai import RAGPipeline
from pathlib import Path

# Initialize RAG
rag = RAGPipeline(collection_name="my_docs")

# Load documents
docs_path = Path("data/documents")
documents = rag.load_documents(docs_path)

# Add to vector store
rag.add_documents(documents)

# Query
result = rag.query("What is the main topic?")
print(result["answer"])
print(f"Sources: {len(result['sources'])}")
```

### 3. Agent Example

```python
from {{ cookiecutter.module_name }}.ai.agent import AIAgent

# Initialize agent
agent = AIAgent(verbose=True)

# Run task
result = agent.run("What is 25 * 17?")
print(result["output"])

# Multi-step reasoning
result = agent.run(
    "Search for information about LangChain, "
    "then calculate how many letters are in the word 'LangChain'"
)
print(result["output"])
```

## Configuration

All configuration is managed via `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-proj-...

# Model selection
MODEL_NAME=gpt-4o              # or gpt-4o-mini, gpt-4-turbo
TEMPERATURE=0.7                # 0.0 = deterministic, 2.0 = creative

# RAG settings
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4

# Agent settings
AGENT_MAX_ITERATIONS=10
AGENT_VERBOSE=true
```

## Best Practices (2026)

### ✅ Do's

1. **Use Pydantic v2** for structured outputs
2. **Version your prompts** in `prompts.py`
3. **Log everything** with loguru
4. **Use environment variables** for secrets
5. **Implement streaming** for better UX
6. **Add metadata** to documents for filtering
7. **Monitor token usage** to control costs
8. **Use hybrid search** (semantic + keyword)

### ❌ Don'ts

1. **Don't hardcode API keys** in code
2. **Don't skip error handling** in production
3. **Don't use outdated models** (e.g., text-davinci-003)
4. **Don't ignore rate limits**
5. **Don't store sensitive data** in vectors
6. **Don't skip input validation**

## Architecture

```
ai/
├── __init__.py          # Public API
├── config.py            # Configuration management
├── prompts.py           # Centralized prompts
├── rag.py              # RAG pipeline
└── agent.py            # AI agents with tools
```

## Advanced Usage

### Custom Tools

Add custom tools to the agent:

```python
from langchain.tools import Tool
from {{ cookiecutter.module_name }}.ai.agent import AIAgent

def custom_tool(query: str) -> str:
    # Your custom logic
    return f"Processed: {query}"

tool = Tool(
    name="CustomTool",
    func=custom_tool,
    description="Description of what this tool does"
)

agent = AIAgent()
agent.add_tool(tool)
```

### Metadata Filtering

Filter documents by metadata:

```python
# Add documents with metadata
docs = [
    Document(
        page_content="...",
        metadata={"source": "doc1.pdf", "category": "finance"}
    )
]
rag.add_documents(docs)

# Query with filter
results = rag.retrieve(
    "What are the key findings?",
    filter_metadata={"category": "finance"}
)
```

### Async Operations

Use async for better performance:

```python
import asyncio
from {{ cookiecutter.module_name }}.ai.agent import AIAgent

async def main():
    agent = AIAgent()
    result = await agent.arun("Calculate 123 * 456")
    print(result["output"])

asyncio.run(main())
```

## Observability

The starter kit includes built-in logging with loguru:

```python
from loguru import logger

# Logs are automatically created for:
# - Configuration loading
# - Document processing
# - Vector store operations
# - Agent reasoning steps
# - Tool executions
# - Errors and warnings
```

## Testing

```bash
# Test configuration
python -m {{ cookiecutter.module_name }}.ai.config

# Test prompts
python -m {{ cookiecutter.module_name }}.ai.prompts

# Test RAG
python -m {{ cookiecutter.module_name }}.ai.rag

# Test agent
python -m {{ cookiecutter.module_name }}.ai.agent
```

## Troubleshooting

### Issue: "OPENAI_API_KEY not set"

**Solution:** Copy `.env.example` to `.env` and add your API key.

### Issue: "ChromaDB collection not found"

**Solution:** The vector store is empty. Add documents first with `rag.add_documents()`.

### Issue: "Rate limit exceeded"

**Solution:** Implement rate limiting or use a different model tier.

### Issue: "Token limit exceeded"

**Solution:** Reduce `chunk_size` or implement token counting before requests.

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## License

Proprietary - See main project LICENSE file.
