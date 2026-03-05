"""
Test fixture: Infinite loop WITH proper break condition
Expected: ✅ Pass - Has explicit termination

This pattern is acceptable because it has clear exit conditions.
"""

from typing import Any

MAX_ITERATIONS = 100


def process_messages(agent: Any) -> None:
    """Process messages with proper termination."""
    iteration = 0
    while True:
        if iteration >= MAX_ITERATIONS:
            break  # Explicit max iteration check
            
        message = agent.get_next_message()
        if message is None:
            break  # Exit when no more messages
            
        response = agent.process(message)
        if response.get("done"):
            break  # Exit on completion signal
            
        agent.send(response)
        iteration += 1


def agent_loop(state: dict) -> dict:
    """Main agent loop with proper termination conditions."""
    max_steps = state.get("max_steps", 50)
    current_step = 0
    
    while True:
        # Multiple exit conditions
        if current_step >= max_steps:
            state["exit_reason"] = "max_steps_reached"
            break
            
        if state.get("goal_achieved"):
            state["exit_reason"] = "goal_achieved"
            break
            
        if state.get("error"):
            state["exit_reason"] = "error"
            break
        
        action = decide_action(state)
        result = execute_action(action)
        state["history"].append(result)
        current_step += 1
    
    return state


def decide_action(state: dict) -> str:
    """Placeholder for action decision."""
    return "continue"


def execute_action(action: str) -> dict:
    """Placeholder for action execution."""
    return {"action": action, "status": "done"}
