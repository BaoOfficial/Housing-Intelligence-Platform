"""
LangGraph ReAct Agent for Housing Intelligence
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import langgraph.prebuilt  # Import module first
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from .tools import AGENT_TOOLS
from .prompts import SYSTEM_PROMPT
from ..config import settings


class HousingAgent:
    """ReAct agent for housing queries with conversation history"""

    def __init__(self):
        """Initialize the ReAct agent"""
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
            streaming=True
        )

        # Initialize memory for conversation history
        self.memory = MemorySaver()

        # Create ReAct agent with tools, system prompt, and memory
        self.agent = create_react_agent(
            self.llm,
            AGENT_TOOLS,
            prompt=SYSTEM_PROMPT,  # Can be string or SystemMessage
            checkpointer=self.memory
        )

    async def ainvoke(self, user_message: str, context: dict = None, thread_id: str = "default"):
        """
        Invoke the ReAct agent asynchronously

        Args:
            user_message: User's question
            context: Additional context (not used in new tool-based approach)
            thread_id: Conversation thread ID for memory

        Returns:
            Agent's response with properties found by tools
        """
        # Configure thread for memory
        config = {"configurable": {"thread_id": thread_id}}

        # Invoke agent with LangGraph API - agent will use search_properties tool
        result = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config
        )

        # Extract final response from messages
        messages = result.get("messages", [])
        response_text = "I apologize, I couldn't process that request."

        if messages:
            last_message = messages[-1]
            response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)

        # Extract search parameters ONLY from the current turn
        # Strategy: Look for tool calls in the LAST few messages only (from this invocation)
        # The result includes old messages + new messages from this turn
        # We'll check the last 10 messages (which should cover any new tool calls)
        search_params = {}

        # Check recent messages for search_properties tool calls
        recent_messages = messages[-10:] if len(messages) > 10 else messages

        for msg in reversed(recent_messages):
            # Look for AIMessage with tool_calls
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    if tool_call.get('name') == 'search_properties':
                        # Found search_properties - take the most recent one
                        search_params = tool_call.get('args', {})
                        break
                if search_params:
                    break

        return {
            "response": response_text,
            "messages": messages,
            "search_params": search_params  # Only params from current turn
        }

    async def astream(self, user_message: str, context: dict = None, thread_id: str = "default"):
        """
        Stream the agent's response

        Args:
            user_message: User's question
            context: Additional context (not used in new tool-based approach)
            thread_id: Conversation thread ID

        Yields:
            Chunks of the agent's response
        """
        # Configure thread for memory
        config = {"configurable": {"thread_id": thread_id}}

        # Stream the response - agent will use search_properties tool
        async for chunk in self.agent.astream(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
            stream_mode="values"
        ):
            yield chunk


# Global agent instance
housing_agent = HousingAgent()
