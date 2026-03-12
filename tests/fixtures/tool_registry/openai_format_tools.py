"""
Test fixture: Tool definitions in OpenAI function-calling dict format
Expected: ✅ Pass — verifier should extract tool names from the "function.name" key
          in each dict, not from decorators.

Registered tools this file defines:
  - search_docs
  - write_file
  - run_tests

These should be detectable without any @tool decorator.
"""

from typing import Any


# OpenAI function-calling format: list of dicts with {"type": "function", "function": {...}}
TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "Search the documentation for relevant information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file at the specified path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "File content"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Execute the project test suite.",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_pattern": {
                        "type": "string",
                        "description": "Pattern to filter tests",
                    }
                },
                "required": [],
            },
        },
    },
]


def execute_tool(name: str, args: dict[str, Any]) -> Any:
    """Dispatch a tool call by name."""
    if name == "search_docs":
        return [{"title": "Doc", "content": "..."}]
    if name == "write_file":
        return {"success": True}
    if name == "run_tests":
        return {"passed": 10, "failed": 0}
    raise ValueError(f"Unknown tool: {name}")
