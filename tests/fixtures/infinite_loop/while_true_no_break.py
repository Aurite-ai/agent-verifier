"""
Test fixture: Infinite loop without break condition
Expected: ⚠️ Warning - Potential infinite loop

This pattern is problematic in AI agents because it can cause:
- Runaway costs (continuous API calls)
- Resource exhaustion
- Unresponsive agents
"""

from typing import Any


def process_messages(agent: Any) -> None:
    """Process messages in an infinite loop - PROBLEMATIC."""
    while True:
        # No break condition - this will run forever
        message = agent.get_next_message()
        response = agent.process(message)
        agent.send(response)
        # Missing: break condition, iteration counter, or timeout


def agent_loop(state: dict) -> dict:
    """Main agent loop without termination - PROBLEMATIC."""
    while True:
        # Continuously process without any exit condition
        action = decide_action(state)
        result = execute_action(action)
        state["history"].append(result)
        # Missing: max iterations check, goal completion check


def decide_action(state: dict) -> str:
    """Placeholder for action decision."""
    return "continue"


def execute_action(action: str) -> dict:
    """Placeholder for action execution."""
    return {"action": action, "status": "done"}
