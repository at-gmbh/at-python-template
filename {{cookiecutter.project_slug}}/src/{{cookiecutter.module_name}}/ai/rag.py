"""
RAG (Retrieval-Augmented Generation) Pipeline

Implements a production-ready RAG system with:
- Document loading and chunking
- Vector embeddings with OpenAI
- ChromaDB for local vector storage
- Semantic search and retrieval
- LLM-based answer generation

Best Practices 2026:
- Hybrid search (semantic + keyword)
- Metadata filtering
- Source attribution
- Streaming responses
- Error handling and fallbacks
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
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from loguru import logger

from .config import get_ai_config
from .prompts import SystemPrompts


class RAGPipeline:
    """
    Production-ready RAG pipeline with ChromaDB vector store.

    Features:
    - Automatic document loading and chunking
    - Persistent vector storage
    - Semantic search with metadata filtering
    - Source attribution in responses
    """

    def __init__(
        self,
        collection_name: str = "default_collection",
        persist_directory: Optional[Path] = None,
    ):
        """
        Initialize RAG pipeline with configuration.

        Args:
            collection_name: Name for the vector store collection
            persist_directory: Directory to persist vector database (default from config)
        """
        self.config = get_ai_config()
        self.collection_name = collection_name
        self.persist_directory = persist_directory or self.config.vector_store_path

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=self.config.embedding_model,
            openai_api_key=self.config.openai_api_key,
        )

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.openai_api_key,
        )

        # Initialize vector store (will load existing if present)
        self.vector_store: Optional[Chroma] = None
        self._load_or_create_vector_store()

        logger.info(
            f"RAG Pipeline initialized: collection={collection_name}, "
            f"persist_dir={self.persist_directory}"
        )

    def _load_or_create_vector_store(self) -> None:
        """Load existing vector store or create new one."""
        try:
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory),
            )
            logger.info(f"Loaded existing vector store: {self.collection_name}")
        except Exception as e:
            logger.warning(f"Could not load vector store: {e}. Creating new one.")
            self.vector_store = None

    def load_documents(
        self,
        source_path: Path,
        file_extensions: Optional[List[str]] = None,
    ) -> List[Document]:
        """
        Load documents from a file or directory.

        Supports:
        - .txt files
        - .pdf files
        - Directory with multiple files

        Args:
            source_path: Path to file or directory
            file_extensions: List of extensions to load (default: ['.txt', '.pdf'])

        Returns:
            List of loaded documents with metadata
        """
        if file_extensions is None:
            file_extensions = [".txt", ".pdf"]

        documents = []

        if source_path.is_file():
            # Load single file
            if source_path.suffix == ".txt":
                loader = TextLoader(str(source_path))
            elif source_path.suffix == ".pdf":
                loader = PyPDFLoader(str(source_path))
            else:
                raise ValueError(f"Unsupported file type: {source_path.suffix}")

            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents from {source_path.name}")

        elif source_path.is_dir():
            # Load from directory
            for ext in file_extensions:
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

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks for embedding.

        Uses RecursiveCharacterTextSplitter with configuration from AIConfig.

        Args:
            documents: List of documents to chunk

        Returns:
            List of chunked documents with preserved metadata
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")

        return chunks

    def add_documents(
        self,
        documents: List[Document],
        chunk: bool = True,
    ) -> None:
        """
        Add documents to the vector store.

        Args:
            documents: Documents to add
            chunk: Whether to chunk documents before adding (recommended)
        """
        if chunk:
            documents = self.chunk_documents(documents)

        if self.vector_store is None:
            # Create new vector store
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=str(self.persist_directory),
            )
        else:
            # Add to existing vector store
            self.vector_store.add_documents(documents)

        logger.info(f"Added {len(documents)} documents to vector store")

    def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query
            k: Number of documents to retrieve (default from config)
            filter_metadata: Metadata filter dict (e.g., {"source": "doc1.pdf"})

        Returns:
            List of relevant documents with similarity scores in metadata
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Add documents first.")

        k = k or self.config.retrieval_k

        search_kwargs = {"k": k}
        if filter_metadata:
            search_kwargs["filter"] = filter_metadata

        retriever = self.vector_store.as_retriever(search_kwargs=search_kwargs)
        documents = retriever.get_relevant_documents(query)

        logger.info(f"Retrieved {len(documents)} documents for query: '{query[:50]}...'")

        return documents

    def generate_answer(
        self,
        query: str,
        context_documents: Optional[List[Document]] = None,
        include_sources: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate an answer to a query using RAG.

        Args:
            query: User's question
            context_documents: Pre-retrieved documents (if None, will retrieve)
            include_sources: Include source documents in response

        Returns:
            Dictionary with 'answer' and optionally 'sources'
        """
        # Retrieve context if not provided
        if context_documents is None:
            context_documents = self.retrieve(query)

        # Build context string
        context = "\n\n".join([doc.page_content for doc in context_documents])

        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", SystemPrompts.RAG_SYSTEM),
            ("user", SystemPrompts.RAG_USER_TEMPLATE),
        ])

        # Create chain
        chain = (
            {
                "context": lambda x: context,
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
        )

        # Generate response
        response = chain.invoke(query)
        answer = response.content

        result = {"answer": answer}

        if include_sources:
            sources = [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata,
                }
                for doc in context_documents
            ]
            result["sources"] = sources

        logger.info(f"Generated answer for query: '{query[:50]}...'")

        return result

    def query(
        self,
        question: str,
        include_sources: bool = True,
    ) -> Dict[str, Any]:
        """
        Convenience method: retrieve and generate answer in one call.

        Args:
            question: User's question
            include_sources: Include source documents in response

        Returns:
            Dictionary with 'answer' and optionally 'sources'
        """
        return self.generate_answer(question, include_sources=include_sources)


# === Example Usage ===

def example_rag_pipeline():
    """
    Example: Build a RAG pipeline and query it.

    This demonstrates the typical workflow:
    1. Initialize pipeline
    2. Load and add documents
    3. Query the system
    """
    # Initialize
    rag = RAGPipeline(collection_name="example_docs")

    # Load documents (example with sample data)
    sample_docs = [
        Document(
            page_content="Python is a high-level programming language created by Guido van Rossum in 1991.",
            metadata={"source": "python_info.txt", "topic": "programming"}
        ),
        Document(
            page_content="LangChain is a framework for building LLM applications with support for RAG and agents.",
            metadata={"source": "langchain_info.txt", "topic": "ai"}
        ),
    ]

    # Add to vector store
    rag.add_documents(sample_docs, chunk=False)

    # Query
    result = rag.query("Who created Python?")
    print(f"Answer: {result['answer']}")
    print(f"\nSources: {len(result['sources'])} documents")


if __name__ == "__main__":
    example_rag_pipeline()
