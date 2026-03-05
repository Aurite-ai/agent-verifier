"""
Test fixture: Tool definitions
Expected: ✅ Pass - Valid tool registry

This file defines the available tools for the agent.
The verification should extract: search_docs, write_file
"""

from typing import Any
from langchain_core.tools import tool


@tool
def search_docs(query: str) -> list[dict]:
    """
    Search the documentation for relevant information.
    
    Args:
        query: The search query string
        
    Returns:
        List of matching documents with title and content
    """
    # Implementation would search actual docs
    return [
        {"title": "Getting Started", "content": "..."},
        {"title": "API Reference", "content": "..."},
    ]


@tool
def write_file(path: str, content: str) -> dict:
    """
    Write content to a file at the specified path.
    
    Args:
        path: File path relative to workspace
        content: Content to write to the file
        
    Returns:
        Status dict with success/failure info
    """
    # Implementation would write to filesystem
    return {"success": True, "path": path, "bytes_written": len(content)}


# Tool defined via schema (alternative pattern)
RUN_TESTS_SCHEMA = {
    "name": "run_tests",
    "description": "Execute the test suite for the project",
    "parameters": {
        "type": "object",
        "properties": {
            "test_pattern": {
                "type": "string",
                "description": "Pattern to filter which tests to run",
            },
            "verbose": {
                "type": "boolean",
                "description": "Whether to show detailed output",
                "default": False,
            },
        },
        "required": [],
    },
}


def run_tests(test_pattern: str = "*", verbose: bool = False) -> dict:
    """Execute tests matching the pattern."""
    return {"passed": 10, "failed": 0, "skipped": 2}


# Registry for reference
AVAILABLE_TOOLS = [
    search_docs,
    write_file,
    # run_tests is defined via schema
]

TOOL_NAMES = ["search_docs", "write_file", "run_tests"]
