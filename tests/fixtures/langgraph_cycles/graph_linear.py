"""
Test fixture: LangGraph graph with no cycle (linear flow)
Expected: ✅ Pass — no cycle, direct path to END

A simple single-node graph that runs once and exits.
No cycle analysis needed; verifier should confirm END is reachable
from the entry point.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    messages: list
    result: str


def agent_node(state: AgentState) -> AgentState:
    """Process the request and return a result."""
    return {**state, "result": "done"}


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)

workflow.set_entry_point("agent")

# Direct edge to END — no cycle possible
workflow.add_edge("agent", END)

app = workflow.compile()
