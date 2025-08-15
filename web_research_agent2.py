from langgraph.prebuilt import create_react_agent

def research_node(state):
    """
    Node logic for web research and recipe enrichment.
    Uses state to extract recipe data, performs web search/enrichment, and updates state.
    """
    recipe_data = state.user_input if hasattr(state, "user_input") else state.get("user_input", {})
    # Simulate web research enrichment (replace with actual web search/LLM call)
    enriched = recipe_data.copy()
    enriched["culture"] = "Italian"  # Example enrichment
    enriched["research_notes"] = "Traditionally made with garlic, olive oil, and pasta."

    state.output = enriched
    return state

# Define the WebResearch agent using LangGraph workflow_graph
web_research_agent = create_react_agent(
    name="WebResearchAgent",
    description="Performs web research and enriches recipe data using workflow_graph.",
    workflow_node=research_node
)