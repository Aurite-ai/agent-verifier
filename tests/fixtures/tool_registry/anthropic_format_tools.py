"""
Test fixture: Tool definitions in Anthropic tool-use dict format
Expected: ✅ Pass — verifier should extract tool names from the top-level "name" key
          in each dict alongside "input_schema".

Registered tools this file defines:
  - search_docs
  - write_file
  - run_tests

These should be detectable without any @tool decorator.
"""

from typing import Any


# Anthropic tool-use format: list of dicts with {"name": ..., "input_schema": {...}}
TOOLS: list[dict[str, Any]] = [
    {
        "name": "search_docs",
        "description": "Search the documentation for relevant information.",
        "input_schema": {
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
    {
        "name": "write_file",
        "description": "Write content to a file at the specified path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "run_tests",
        "description": "Execute the project test suite.",
        "input_schema": {
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
]


def execute_tool(tool_name: str, tool_input: dict[str, Any]) -> Any:
    """Dispatch a tool call by name."""
    if tool_name == "search_docs":
        return [{"title": "Doc", "content": "..."}]
    if tool_name == "write_file":
        return {"success": True}
    if tool_name == "run_tests":
        return {"passed": 10, "failed": 0}
    raise ValueError(f"Unknown tool: {tool_name}")
