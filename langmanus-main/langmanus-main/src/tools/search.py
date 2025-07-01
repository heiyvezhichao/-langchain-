import logging
import os
from typing import Any
from langchain_community.tools.tavily_search import TavilySearchResults
from src.config import TAVILY_MAX_RESULTS
from .decorators import create_logged_tool

logger = logging.getLogger(__name__)

# Initialize Tavily search tool with logging
LoggedTavilySearch = create_logged_tool(TavilySearchResults)

# Check if Tavily API key is available
if os.environ.get("TAVILY_API_KEY"):
    tavily_tool = LoggedTavilySearch(name="tavily_search", max_results=TAVILY_MAX_RESULTS)
else:
    # Create a mock Tavily search tool that returns a message about missing API key
    from langchain_core.tools import BaseTool, tool
    
    @tool
    def tavily_search(query: str) -> str:
        """Search the web for information (Unavailable - Missing API key)"""
        return "Tavily search is unavailable. Please set TAVILY_API_KEY in your .env file."
    
    tavily_tool = tavily_search
    logger.warning("No Tavily API key found. Using mock search tool instead.")
