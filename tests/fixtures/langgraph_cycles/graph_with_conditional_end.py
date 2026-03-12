"""
Test fixture: LangGraph graph with cycle and conditional exit
Expected: ✅ Pass — cycle exists but END is reachable via conditional edge

The graph loops agent → tools → agent, but the "agent" node has a
conditional edge whose mapping includes END as a possible destination.
The cycle is safe because the routing function can terminate it.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    messages: list
    iteration: int
    max_iterations: int


def should_continue(state: AgentState) -> Literal["continue", "end"]:
    """Route to tools or END based on iteration count and goal."""
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    if state.get("goal_achieved"):
        return "end"
    return "continue"


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

# Conditional edge from "agent": can route to "tools" (continue) or END
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,          # END is reachable — cycle is bounded
    },
)

# Unconditional back-edge from tools to agent (creates the cycle)
workflow.add_edge("tools", "agent")

app = workflow.compile()
