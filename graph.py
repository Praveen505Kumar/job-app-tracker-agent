"""Builds the pipeline graph: scanner -> extractor -> tracker."""

from functools import partial

from agents.extractor import extractor_node
from agents.scanner import scanner_node
from agents.tracker import tracker_node
from langgraph.graph import END, StateGraph
from state import AgentState


def build_graph(mcp_tools: dict):
    graph = StateGraph(AgentState)

    # scanner needs the live MCP tools, so bind them in via partial
    graph.add_node("scanner", partial(scanner_node, mcp_tools=mcp_tools))
    graph.add_node("extractor", extractor_node)
    graph.add_node("tracker", tracker_node)

    graph.set_entry_point("scanner")
    graph.add_edge("scanner", "extractor")
    graph.add_edge("extractor", "tracker")
    graph.add_edge("tracker", END)

    return graph.compile()
