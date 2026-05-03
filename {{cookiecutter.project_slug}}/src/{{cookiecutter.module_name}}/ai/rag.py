"""
RAG (Retrieval-Augmented Generation) - Simple & Transparent

🎯 PHILOSOPHY: "Show, don't hide"

This module provides a MINIMAL RAG setup using LangChain directly.
NO complex wrapper classes - just clean, readable functions that you can
easily customize.

🚀 CUSTOMIZATION POINTS:
1. build_rag_chain() - Swap retriever, change prompts
2. load_documents() - Add new document loaders
3. create_retriever() - Try different retrieval strategies

Think of this as a TEMPLATE, not a framework. Copy-paste and modify!

Best Practices 2026:
- Transparent LangChain usage (no magic)
- Easy to understand, easy to modify
- Comments point to customization opportunities
"""

from pathlib import Path
from typing import List, Optional, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
)
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from loguru import logger

from .config import get_ai_config


# =============================================================================
# DOCUMENT LOADING - Customize for your data sources
# =============================================================================

def load_documents(
    source_path: Path,
    file_extensions: Optional[List[str]] = None,
) -> List[Document]:
    """
    Load documents from files or directories.

    🚀 TODO: Add your custom loaders here!
    - Add CSV loader for tabular data
    - Add API loader for external data
    - Add database loader for SQL data

    Args:
        source_path: Path to file or directory
        file_extensions: Extensions to load (default: ['.txt', '.pdf'])

    Returns:
        List of loaded documents with metadata

    Example:
        # Load single file
        docs = load_documents(Path("data/report.pdf"))

        # Load directory
        docs = load_documents(Path("data/"), [".txt", ".md"])
    """
    if file_extensions is None:
        file_extensions = [".txt", ".pdf"]

    documents = []

    if source_path.is_file():
        # Single file loading
        if source_path.suffix == ".txt":
            loader = TextLoader(str(source_path))
        elif source_path.suffix == ".pdf":
            loader = PyPDFLoader(str(source_path))
        else:
            raise ValueError(f"Unsupported file type: {source_path.suffix}")

        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {source_path.name}")

    elif source_path.is_dir():
        # Directory loading
        for ext in file_extensions:
            # TODO: Customize glob pattern if needed (e.g., "**/*.txt" for recursive)
            if ext == ".txt":
                loader = DirectoryLoader(
                    str(source_path),
                    glob=f"**/*{ext}",
                    loader_cls=TextLoader,
                )
            elif ext == ".pdf":
                loader = DirectoryLoader(
                    str(source_path),
                    glob=f"**/*{ext}",
                    loader_cls=PyPDFLoader,
                )
            else:
                continue

            docs = loader.load()
            documents.extend(docs)

        logger.info(f"Loaded {len(documents)} documents from {source_path}")

    else:
        raise ValueError(f"Invalid source path: {source_path}")

    return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """
    Split documents into chunks for embedding.

    🚀 TODO: Customize chunking strategy
    - Try CharacterTextSplitter for simpler splitting
    - Try TokenTextSplitter for token-aware splitting
    - Adjust separators for your document structure

    Args:
        documents: Documents to chunk
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of chunked documents
    """
    # TODO: Customize separators based on your document structure
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],  # Customize this!
    )

    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")

    return chunks


# =============================================================================
# VECTOR STORE & RETRIEVAL - Swap ChromaDB if needed
# =============================================================================

def create_vector_store(
    documents: List[Document],
    collection_name: str = "default",
    persist_directory: Optional[Path] = None,
) -> Chroma:
    """
    Create or update vector store with documents.

    🚀 TODO: Try different vector stores
    - FAISS for in-memory (faster)
    - Pinecone for production scale
    - Weaviate for advanced features

    Args:
        documents: Chunked documents to embed
        collection_name: Name for the collection
        persist_directory: Where to save the vector DB

    Returns:
        ChromaDB vector store
    """
    config = get_ai_config()

    if persist_directory is None:
        persist_directory = config.vector_store_path

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model=config.embedding_model,
        openai_api_key=config.openai_api_key,
    )

    # TODO: Try creating from scratch vs. loading existing
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=str(persist_directory),
    )

    logger.info(f"Created vector store: {collection_name} with {len(documents)} docs")

    return vector_store


def create_retriever(
    vector_store: Chroma,
    k: int = 4,
    search_type: str = "similarity",
) -> Any:
    """
    Create retriever from vector store.

    🚀 TODO: Experiment with retrieval strategies
    - similarity: Standard cosine similarity
    - mmr: Maximum Marginal Relevance (diversity)
    - similarity_score_threshold: Filter by score

    Args:
        vector_store: Vector store to retrieve from
        k: Number of documents to retrieve
        search_type: Type of search (similarity, mmr)

    Returns:
        LangChain retriever
    """
    # TODO: Add metadata filtering if needed
    # search_kwargs = {"k": k, "filter": {"category": "finance"}}

    retriever = vector_store.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k}
    )

    logger.info(f"Created retriever: type={search_type}, k={k}")

    return retriever


# =============================================================================
# RAG CHAIN - This is where you customize the magic!
# =============================================================================

def build_rag_chain(
    retriever: Any,
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    custom_prompt: Optional[str] = None,
):
    """
    Build RAG chain using LCEL (LangChain Expression Language).

    🎯 THIS IS THE CORE! Customize this to fit your needs.

    🚀 CUSTOMIZATION IDEAS:
    - Change the prompt template
    - Add context compression
    - Add re-ranking step
    - Add output parsing/validation
    - Add conversation memory

    Args:
        retriever: Document retriever
        model_name: Override default model
        temperature: Override default temperature
        custom_prompt: Custom system prompt

    Returns:
        Runnable RAG chain

    Example:
        # Build and use
        chain = build_rag_chain(retriever)
        response = chain.invoke("What is RAG?")
    """
    config = get_ai_config()

    # Use provided params or defaults
    model_name = model_name or config.model_name
    temperature = temperature if temperature is not None else config.temperature

    # Initialize LLM
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=config.openai_api_key,
    )

    # TODO: CUSTOMIZE THIS PROMPT!
    # This is where you define how the AI uses retrieved context
    system_prompt = custom_prompt or """You are a helpful AI assistant with access to a knowledge base.

Use the provided context to answer questions accurately and concisely.

If the context doesn't contain relevant information, say so clearly.

Context:
{context}

Question: {question}"""

    prompt = ChatPromptTemplate.from_template(system_prompt)

    # Build the RAG chain using LCEL
    # TODO: Add more steps if needed (e.g., context compression, re-ranking)
    rag_chain = (
        {
            "context": retriever | format_docs,  # Retrieve and format
            "question": RunnablePassthrough()    # Pass question through
        }
        | prompt                                 # Fill prompt template
        | llm                                    # Generate response
        | StrOutputParser()                      # Parse output
    )

    logger.info(f"Built RAG chain: model={model_name}, temp={temperature}")

    return rag_chain


def format_docs(docs: List[Document]) -> str:
    """
    Format retrieved documents for the prompt.

    🚀 TODO: Customize formatting
    - Add document metadata
    - Add source attribution
    - Limit context length
    """
    return "\n\n".join(doc.page_content for doc in docs)


# =============================================================================
# CONVENIENCE FUNCTIONS - High-level API for quick usage
# =============================================================================

def simple_rag_query(
    question: str,
    docs_path: Path,
    collection_name: str = "default",
) -> Dict[str, Any]:
    """
    One-shot RAG query - Load docs, build chain, query.

    🎯 USE THIS for quick experiments!

    For production, build the chain once and reuse it.

    Args:
        question: User's question
        docs_path: Path to documents
        collection_name: Vector store collection name

    Returns:
        Dict with answer and metadata

    Example:
        result = simple_rag_query(
            "What is the main topic?",
            Path("data/documents/")
        )
        print(result["answer"])
    """
    logger.info(f"Simple RAG query: {question[:50]}...")

    # Load and chunk documents
    documents = load_documents(docs_path)
    chunks = chunk_documents(documents)

    # Create vector store and retriever
    vector_store = create_vector_store(chunks, collection_name)
    retriever = create_retriever(vector_store)

    # Build and run chain
    chain = build_rag_chain(retriever)
    answer = chain.invoke(question)

    # Get source documents
    source_docs = retriever.get_relevant_documents(question)

    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content[:200],
                "metadata": doc.metadata
            }
            for doc in source_docs
        ],
        "num_sources": len(source_docs),
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    """
    Demo: How to use the RAG functions

    🎯 Run this to test your setup!
    """
    # Example 1: Simple query
    print("=== Example 1: Simple RAG Query ===")

    # Create sample documents
    sample_docs = [
        Document(
            page_content="Python was created by Guido van Rossum in 1991.",
            metadata={"source": "python_history.txt"}
        ),
        Document(
            page_content="LangChain is a framework for building LLM applications with RAG support.",
            metadata={"source": "langchain_info.txt"}
        ),
    ]

    # Build RAG chain
    vector_store = create_vector_store(sample_docs, "demo")
    retriever = create_retriever(vector_store, k=2)
    chain = build_rag_chain(retriever)

    # Query
    question = "Who created Python?"
    answer = chain.invoke(question)

    print(f"Q: {question}")
    print(f"A: {answer}")

    # Example 2: Custom parameters
    print("\n=== Example 2: Custom Temperature ===")

    creative_chain = build_rag_chain(
        retriever,
        temperature=1.5,  # More creative
        custom_prompt="You are a friendly teacher. Explain in simple terms:\n\nContext: {context}\n\nQuestion: {question}"
    )

    answer = creative_chain.invoke(question)
    print(f"A (creative): {answer}")

    print("\n✅ RAG setup working! Now customize it for your use case.")
