{% if cookiecutter.ui_framework == 'chainlit' -%}
"""
Chainlit Chat Interface for AI Application

This module provides an async chatbot interface using Chainlit.

Features:
- Async message handling
- Streaming responses
- Session management
- RAG integration

Usage:
    chainlit run src/{{ cookiecutter.module_name }}/ui/app.py

Environment Variables:
    OPENAI_API_KEY: OpenAI API key (required)
    MODEL_NAME: Model to use (default: gpt-4o)
"""

import os
from pathlib import Path

import chainlit as cl
from loguru import logger

{%- if cookiecutter.include_ai_starter_kit == 'yes' %}
from {{ cookiecutter.module_name }}.ai.config import get_ai_config
from {{ cookiecutter.module_name }}.ai.rag import RAGPipeline
{%- endif %}


@cl.on_chat_start
async def on_chat_start():
    """
    Initialize chat session when a new user connects.

    Sets up:
    - AI configuration
    - RAG pipeline
    - Welcome message
    """
    logger.info("New chat session started")

    {%- if cookiecutter.include_ai_starter_kit == 'yes' %}
    try:
        # Initialize AI config
        config = get_ai_config()
        logger.info(f"AI Config loaded: model={config.model_name}")

        # Initialize RAG pipeline
        rag = RAGPipeline(collection_name="chat_documents")

        # Store in session
        cl.user_session.set("rag", rag)
        cl.user_session.set("config", config)

        await cl.Message(
            content="👋 Welcome! I'm your AI assistant powered by LangChain and ChromaDB.\n\n"
                    "You can ask me questions and I'll use RAG to provide accurate answers.\n\n"
                    "**Try asking:**\n"
                    "- Questions about your documents\n"
                    "- General knowledge queries\n"
                    "- For help with calculations or data"
        ).send()

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        await cl.Message(
            content="⚠️ Configuration Error\n\n"
                    f"Please check your environment variables:\n"
                    f"```\n{str(e)}\n```\n\n"
                    "Copy `.env.example` to `.env` and add your OpenAI API key."
        ).send()
        raise
    {%- else %}
    await cl.Message(
        content="👋 Welcome to {{ cookiecutter.project_name }}!\n\n"
                "This is a Chainlit chatbot interface.\n\n"
                "Enable the AI Starter Kit during project generation to add RAG capabilities."
    ).send()
    {%- endif %}


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming user messages.

    Args:
        message: User's message from Chainlit
    """
    user_query = message.content
    logger.info(f"Received message: {user_query[:50]}...")

    {%- if cookiecutter.include_ai_starter_kit == 'yes' %}
    # Get RAG pipeline from session
    rag: RAGPipeline = cl.user_session.get("rag")

    if not rag:
        await cl.Message(content="⚠️ RAG pipeline not initialized. Please refresh.").send()
        return

    # Create response message
    response_msg = cl.Message(content="")

    try:
        # Query RAG pipeline
        result = rag.query(user_query, include_sources=True)

        # Send answer
        response_msg.content = result["answer"]

        # Add sources if available
        if result.get("sources"):
            sources_text = "\n\n**Sources:**\n"
            for i, source in enumerate(result["sources"][:3], 1):
                sources_text += f"{i}. {source['content'][:100]}...\n"
            response_msg.content += sources_text

        await response_msg.send()

        logger.info("Response sent successfully")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await cl.Message(
            content=f"⚠️ An error occurred while processing your request:\n```\n{str(e)}\n```"
        ).send()
    {%- else %}
    # Echo back without AI (placeholder)
    await cl.Message(
        content=f"You said: {user_query}\n\n"
                "Enable the AI Starter Kit to add intelligent responses."
    ).send()
    {%- endif %}


@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end."""
    logger.info("Chat session ended")


if __name__ == "__main__":
    # For development: Run with `python -m {{ cookiecutter.module_name }}.ui.app`
    # For production: Run with `chainlit run src/{{ cookiecutter.module_name }}/ui/app.py`
    import sys
    print("Please run with: chainlit run src/{{ cookiecutter.module_name }}/ui/app.py")
    sys.exit(1)

{%- elif cookiecutter.ui_framework == 'streamlit' -%}
"""
Streamlit Chat Interface for AI Application

This module provides a chat interface using Streamlit.

Features:
- Chat history
- Streaming responses (optional)
- Session state management
- RAG integration

Usage:
    streamlit run src/{{ cookiecutter.module_name }}/ui/app.py

Environment Variables:
    OPENAI_API_KEY: OpenAI API key (required)
    MODEL_NAME: Model to use (default: gpt-4o)
"""

import os
from pathlib import Path

import streamlit as st
from loguru import logger

{%- if cookiecutter.include_ai_starter_kit == 'yes' %}
from {{ cookiecutter.module_name }}.ai.config import get_ai_config
from {{ cookiecutter.module_name }}.ai.rag import RAGPipeline
{%- endif %}


def initialize_session():
    """Initialize Streamlit session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    {%- if cookiecutter.include_ai_starter_kit == 'yes' %}
    if "rag" not in st.session_state:
        try:
            config = get_ai_config()
            rag = RAGPipeline(collection_name="streamlit_documents")
            st.session_state.rag = rag
            st.session_state.config = config
            logger.info(f"RAG initialized: model={config.model_name}")
        except ValueError as e:
            st.error(f"⚠️ Configuration Error: {e}")
            st.info("Copy `.env.example` to `.env` and add your OpenAI API key.")
            st.stop()
    {%- endif %}


def main():
    """Main Streamlit application."""

    # Page config
    st.set_page_config(
        page_title="{{ cookiecutter.project_name }}",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize session
    initialize_session()

    # Sidebar
    with st.sidebar:
        st.title("🤖 {{ cookiecutter.project_name }}")
        st.markdown("---")

        {%- if cookiecutter.include_ai_starter_kit == 'yes' %}
        st.subheader("Configuration")
        if "config" in st.session_state:
            config = st.session_state.config
            st.info(f"**Model:** {config.model_name}")
            st.info(f"**Temperature:** {config.temperature}")

        st.markdown("---")
        st.subheader("About")
        st.markdown(
            "This chatbot uses **RAG** (Retrieval-Augmented Generation) "
            "with LangChain and ChromaDB to answer questions based on your documents."
        )
        {%- else %}
        st.info("Enable the AI Starter Kit to add RAG capabilities.")
        {%- endif %}

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    st.title("💬 Chat")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            {%- if cookiecutter.include_ai_starter_kit == 'yes' %}
            try:
                rag: RAGPipeline = st.session_state.rag

                with st.spinner("Thinking..."):
                    result = rag.query(prompt, include_sources=True)

                # Display answer
                response = result["answer"]
                st.markdown(response)

                # Display sources
                if result.get("sources"):
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(result["sources"][:3], 1):
                            st.markdown(f"**{i}.** {source['content'][:200]}...")

                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                logger.info(f"Response generated for query: {prompt[:50]}...")

            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.error(error_msg)
                logger.error(f"Error generating response: {e}")
            {%- else %}
            response = f"You said: {prompt}\n\nEnable the AI Starter Kit to add intelligent responses."
            st.markdown(response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            {%- endif %}


if __name__ == "__main__":
    main()

{%- else -%}
"""
Placeholder UI Module

No UI framework selected during project generation.

To add a UI framework:
1. Re-generate the project with `ui_framework` set to 'chainlit' or 'streamlit'
2. Or manually install and configure your preferred UI framework
"""

def main():
    print("No UI framework configured.")
    print("Re-generate the project with ui_framework='chainlit' or 'streamlit'")

if __name__ == "__main__":
    main()
{%- endif %}
