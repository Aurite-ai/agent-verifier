"""
Test fixture: LangGraph graph with infinite cycle
Expected: ❌ Issue — cycle between "agent" and "tools" nodes with no path to END

The graph loops agent → tools → agent indefinitely.
Neither node has a conditional edge that can route to END.
This will run forever on any input.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    messages: list
    iteration: int


def agent_node(state: AgentState) -> AgentState:
    """Decide next action."""
    return {**state, "iteration": state["iteration"] + 1}


def tool_node(state: AgentState) -> AgentState:
    """Execute a tool."""
    return state


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

# Unconditional cycle: agent → tools → agent, no way out
workflow.add_edge("agent", "tools")
workflow.add_edge("tools", "agent")

# Missing: conditional edge from "agent" that can route to END

app = workflow.compile()
