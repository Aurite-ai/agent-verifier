"""
Test fixture: Recursive function without clear base case
Expected: ⚠️ Warning - Potential infinite recursion

Recursive agent patterns need explicit termination to prevent:
- Stack overflow
- Runaway API costs
- Memory exhaustion
"""

from typing import Any


def process_task(task: dict, agent: Any) -> dict:
    """
    Recursively process task and subtasks - PROBLEMATIC.
    
    The base case check is too weak - relies on external state
    that may never become falsy.
    """
    # Weak base case - depends on task structure being correct
    result = agent.execute(task)
    
    # Always recurses if there are subtasks, no depth limit
    if result.get("subtasks"):
        for subtask in result["subtasks"]:
            # Recursive call without depth tracking
            process_task(subtask, agent)
    
    return result


def expand_thought(thought: str, agent: Any) -> list[str]:
    """
    Recursively expand thoughts - PROBLEMATIC.
    
    No maximum depth, relies on agent to eventually return
    empty expansions (which may never happen).
    """
    expansions = agent.expand(thought)
    
    all_thoughts = [thought]
    for expansion in expansions:
        # Unbounded recursion
        all_thoughts.extend(expand_thought(expansion, agent))
    
    return all_thoughts


def search_tree(node: dict, target: str) -> dict | None:
    """
    Recursive tree search - PROBLEMATIC.
    
    No cycle detection, no depth limit. Could loop forever
    on cyclic graph structures.
    """
    if node.get("value") == target:
        return node
    
    for child in node.get("children", []):
        # No visited set, no max depth
        result = search_tree(child, target)
        if result:
            return result
    
    return None
