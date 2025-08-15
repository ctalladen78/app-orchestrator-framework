from langgraph.graph import StateGraph, END, START

# Assume AgentState is your state class, and node functions are defined elsewhere
from agent_supervisor import supervisor_agent
from web_research_agent import research_node
from aws_agent import query_search_node

# Create the workflow graph
workflow = StateGraph(AgentState)

# Supervisor node: detects user intent and routes to the right agent
workflow.add_node("Supervisor", supervisor_agent)

# Researcher node: handles web research and recipe enrichment
workflow.add_node("Researcher", research_node)

# Query_search node: handles AWS database queries (DynamoDB, etc.)
workflow.add_node("Query_search", query_search_node)

# Sample: add edges (define flow)
workflow.add_edge(START, "Supervisor")
workflow.add_edge("Supervisor", "Researcher")      # For make_new_recipe intent
workflow.add_edge("Supervisor", "Query_search")    # For get_recipes intent
workflow.add_edge("Researcher", END)
workflow.add_edge("Query_search", END)

# Save or visualize workflow as needed