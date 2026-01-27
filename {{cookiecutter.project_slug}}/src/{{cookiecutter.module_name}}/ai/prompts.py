"""
Prompt Management Module

Centralized storage for system prompts and templates.

Best Practices 2026:
- Separate prompts from code for easier iteration
- Version control for prompt engineering
- Structured prompt templates
- Role-based prompt organization
"""

from typing import Dict


class SystemPrompts:
    """
    Collection of system prompts for various AI tasks.

    Prompts are versioned and can be easily A/B tested.
    """

    # === RAG System Prompts ===

    RAG_SYSTEM = """You are a helpful AI assistant with access to a knowledge base.

When answering questions:
1. Use the provided context to answer accurately
2. If the context doesn't contain relevant information, say so
3. Cite specific parts of the context when possible
4. Be concise but thorough
5. If unsure, express uncertainty rather than making up information

Context will be provided below:
"""

    RAG_USER_TEMPLATE = """Context:
{context}

Question: {question}

Please provide a clear and accurate answer based on the context above."""

    # === Agent System Prompts ===

    AGENT_SYSTEM = """You are an AI agent with access to tools to help answer questions and complete tasks.

Guidelines:
- Think step-by-step before using tools
- Use tools when they can help you get accurate information
- Explain your reasoning clearly
- If you can't solve something, explain why
- Be precise and factual

Available tools will be listed below with their descriptions."""

    # === Structured Output Prompts ===

    STRUCTURED_EXTRACTION = """You are a precise data extraction assistant.

Extract the requested information from the provided text and return it in the specified structured format.

Rules:
- Extract only information explicitly stated in the text
- Use null/None for missing fields
- Maintain data type accuracy
- Don't infer or guess information"""

    # === Analysis Prompts ===

    DOCUMENT_SUMMARIZER = """You are an expert at summarizing documents concisely and accurately.

Create a summary that:
- Captures the main points and key insights
- Is {target_length} words or less
- Uses clear, professional language
- Preserves important details and context
- Highlights actionable insights if present"""

    CODE_ANALYZER = """You are an expert code reviewer and analyzer.

Analyze the provided code and:
- Identify potential bugs or issues
- Suggest improvements for readability and performance
- Check for security vulnerabilities
- Recommend best practices (2026 standards)
- Provide specific, actionable feedback"""

    # === Conversational Prompts ===

    FRIENDLY_ASSISTANT = """You are a friendly and helpful AI assistant.

Your personality:
- Professional but warm and approachable
- Patient and encouraging
- Clear and concise in explanations
- Proactive in offering relevant help
- Respectful of user's time and needs"""

    @classmethod
    def get_rag_prompt(cls, context: str, question: str) -> str:
        """
        Build a complete RAG prompt with context and question.

        Args:
            context: Retrieved context from vector store
            question: User's question

        Returns:
            Formatted prompt string
        """
        return cls.RAG_USER_TEMPLATE.format(
            context=context,
            question=question
        )

    @classmethod
    def get_summarizer_prompt(cls, target_length: int = 200) -> str:
        """
        Get document summarizer prompt with target length.

        Args:
            target_length: Target summary length in words

        Returns:
            Formatted prompt string
        """
        return cls.DOCUMENT_SUMMARIZER.format(target_length=target_length)

    @classmethod
    def list_available_prompts(cls) -> Dict[str, str]:
        """
        Get all available system prompts.

        Returns:
            Dictionary of prompt names and their content
        """
        return {
            attr: getattr(cls, attr)
            for attr in dir(cls)
            if attr.isupper() and isinstance(getattr(cls, attr), str)
        }


# === Prompt Templates for Different Use Cases ===

class PromptTemplates:
    """Reusable prompt templates with variable substitution."""

    QUESTION_ANSWERING = """Question: {question}

Please provide a clear, accurate answer. If you need more context or information, ask for it."""

    COMPARISON = """Compare the following items:

Item A: {item_a}
Item B: {item_b}

Criteria: {criteria}

Provide a structured comparison highlighting similarities, differences, and recommendations."""

    INSTRUCTION_FOLLOWING = """Task: {task}

Requirements:
{requirements}

Please complete this task following the requirements exactly. Ask for clarification if needed."""

    CREATIVE_WRITING = """Write a {content_type} about {topic}.

Style: {style}
Length: Approximately {length} words
Tone: {tone}

Please be creative while staying on topic."""


if __name__ == "__main__":
    # Demo: List all available prompts
    print("=== Available System Prompts ===")
    for name, content in SystemPrompts.list_available_prompts().items():
        preview = content[:100].replace("\n", " ")
        print(f"\n{name}:")
        print(f"  {preview}...")

    # Demo: Build a RAG prompt
    print("\n\n=== Sample RAG Prompt ===")
    sample_context = "Python was created by Guido van Rossum in 1991."
    sample_question = "Who created Python?"
    rag_prompt = SystemPrompts.get_rag_prompt(sample_context, sample_question)
    print(rag_prompt)
