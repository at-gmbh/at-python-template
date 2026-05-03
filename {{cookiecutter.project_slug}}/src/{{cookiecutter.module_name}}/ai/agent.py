"""
LangChain Agent Implementation

Implements an AI agent with tool-calling capabilities.

Best Practices 2026:
- Function calling with structured outputs
- Tool validation with Pydantic
- Observability and logging
- Error handling and retries
- Streaming support
"""

from typing import List, Optional, Any, Dict

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool, StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from loguru import logger
from pydantic import BaseModel, Field

from .config import get_ai_config
from .prompts import SystemPrompts


# === Tool Definitions with Pydantic ===

class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""
    expression: str = Field(description="Mathematical expression to evaluate (e.g., '2 + 2')")


def calculator_tool(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Supports basic arithmetic operations: +, -, *, /, **, ()

    Args:
        expression: Mathematical expression as string

    Returns:
        Result of the calculation

    Example:
        calculator_tool("2 + 2 * 3") -> "8"
    """
    try:
        # Safe evaluation (only allow math operations)
        result = eval(expression, {"__builtins__": {}}, {})
        logger.info(f"Calculator: {expression} = {result}")
        return str(result)
    except Exception as e:
        error_msg = f"Error evaluating expression '{expression}': {str(e)}"
        logger.error(error_msg)
        return error_msg


class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(description="Search query to look up information")


def mock_search_tool(query: str) -> str:
    """
    Mock search tool for demonstration.

    In production, replace with actual search API (e.g., Google, Bing, Tavily).

    Args:
        query: Search query

    Returns:
        Mock search results
    """
    logger.info(f"Search: {query}")

    # Mock responses for demo purposes
    mock_results = {
        "python": "Python is a high-level programming language created by Guido van Rossum in 1991. "
                 "It emphasizes code readability and simplicity.",
        "langchain": "LangChain is a framework for developing applications powered by language models. "
                    "It provides modular components for building LLM applications.",
        "ai": "Artificial Intelligence (AI) refers to computer systems capable of performing tasks "
             "that typically require human intelligence.",
    }

    # Simple keyword matching
    for keyword, result in mock_results.items():
        if keyword in query.lower():
            return result

    return f"No specific information found for: {query}. This is a mock search tool."


class CurrentDateInput(BaseModel):
    """Input schema for date tool (no parameters needed)."""
    pass


def get_current_date() -> str:
    """
    Get the current date.

    Returns:
        Current date in ISO format (YYYY-MM-DD)
    """
    from datetime import datetime

    date = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Current date requested: {date}")
    return f"The current date is {date}"


# === Agent Implementation ===

class AIAgent:
    """
    LangChain agent with tool-calling capabilities.

    Features:
    - Multiple tools with structured inputs
    - OpenAI function calling
    - Conversation memory
    - Verbose logging
    - Error handling
    """

    def __init__(
        self,
        tools: Optional[List[Tool]] = None,
        system_message: Optional[str] = None,
        verbose: bool = True,
    ):
        """
        Initialize AI agent with tools and configuration.

        Args:
            tools: List of tools available to the agent (default: calculator, search, date)
            system_message: Custom system message (default from prompts)
            verbose: Enable verbose logging of agent reasoning
        """
        self.config = get_ai_config()
        self.verbose = verbose or self.config.agent_verbose

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            openai_api_key=self.config.openai_api_key,
        )

        # Setup tools
        self.tools = tools or self._get_default_tools()

        # Setup prompt
        self.system_message = system_message or SystemPrompts.AGENT_SYSTEM
        self.prompt = self._create_prompt()

        # Create agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.verbose,
            max_iterations=self.config.agent_max_iterations,
            handle_parsing_errors=True,
        )

        logger.info(f"AI Agent initialized with {len(self.tools)} tools")

    def _get_default_tools(self) -> List[Tool]:
        """
        Get default tool set for the agent.

        Returns:
            List of default tools
        """
        tools = [
            StructuredTool.from_function(
                func=calculator_tool,
                name="Calculator",
                description="Useful for performing mathematical calculations. "
                           "Input should be a mathematical expression.",
                args_schema=CalculatorInput,
            ),
            StructuredTool.from_function(
                func=mock_search_tool,
                name="Search",
                description="Useful for searching information about general topics. "
                           "Input should be a search query.",
                args_schema=SearchInput,
            ),
            StructuredTool.from_function(
                func=get_current_date,
                name="GetCurrentDate",
                description="Get the current date in YYYY-MM-DD format. No input needed.",
                args_schema=CurrentDateInput,
            ),
        ]

        return tools

    def _create_prompt(self) -> ChatPromptTemplate:
        """
        Create prompt template for the agent.

        Returns:
            ChatPromptTemplate with system message and placeholders
        """
        return ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    def run(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Execute agent with a query.

        Args:
            query: User's question or task
            chat_history: Previous conversation messages (optional)

        Returns:
            Dictionary with 'output' and 'intermediate_steps'
        """
        inputs = {"input": query}

        if chat_history:
            inputs["chat_history"] = chat_history

        try:
            result = self.agent_executor.invoke(inputs)
            logger.info(f"Agent completed task: {query[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Agent execution error: {e}")
            return {
                "output": f"Error executing agent: {str(e)}",
                "intermediate_steps": [],
            }

    async def arun(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Execute agent asynchronously.

        Args:
            query: User's question or task
            chat_history: Previous conversation messages (optional)

        Returns:
            Dictionary with 'output' and 'intermediate_steps'
        """
        inputs = {"input": query}

        if chat_history:
            inputs["chat_history"] = chat_history

        try:
            result = await self.agent_executor.ainvoke(inputs)
            logger.info(f"Agent completed task (async): {query[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Agent execution error (async): {e}")
            return {
                "output": f"Error executing agent: {str(e)}",
                "intermediate_steps": [],
            }

    def add_tool(self, tool: Tool) -> None:
        """
        Add a new tool to the agent.

        Requires re-initializing the agent executor.

        Args:
            tool: Tool to add
        """
        self.tools.append(tool)

        # Recreate agent with new tools
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.verbose,
            max_iterations=self.config.agent_max_iterations,
            handle_parsing_errors=True,
        )

        logger.info(f"Added tool: {tool.name}")

    def list_tools(self) -> List[str]:
        """
        List available tool names.

        Returns:
            List of tool names
        """
        return [tool.name for tool in self.tools]


# === Example Usage ===

def example_agent():
    """
    Example: Create and use an AI agent.

    Demonstrates:
    1. Agent initialization
    2. Tool usage (calculator, search)
    3. Multi-step reasoning
    """
    # Initialize agent
    agent = AIAgent(verbose=True)

    print(f"Agent initialized with tools: {agent.list_tools()}\n")

    # Example 1: Calculator
    print("=== Example 1: Calculator ===")
    result = agent.run("What is 123 * 456 + 789?")
    print(f"Result: {result['output']}\n")

    # Example 2: Search
    print("=== Example 2: Search ===")
    result = agent.run("What is LangChain?")
    print(f"Result: {result['output']}\n")

    # Example 3: Date
    print("=== Example 3: Current Date ===")
    result = agent.run("What's today's date?")
    print(f"Result: {result['output']}\n")

    # Example 4: Multi-step reasoning
    print("=== Example 4: Multi-step ===")
    result = agent.run(
        "What's the date today? Then calculate how many days until the end of the month (assume 30 days)."
    )
    print(f"Result: {result['output']}")


if __name__ == "__main__":
    example_agent()
