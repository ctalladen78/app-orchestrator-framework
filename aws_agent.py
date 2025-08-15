from workflow_graph import workflow
from langgraph.prebuilt import create_react_agent

def query_search_node(state):
    """
    Node logic for querying AWS database.
    Uses state to extract search parameters and returns query results.
    """
    user_input = state.user_input
    recipe_name = user_input.get("target") if isinstance(user_input, dict) else user_input

    # Simulate DynamoDB query payload
    query_payload = {
        "KeyConditionExpression": "food_name = :r",
        "ExpressionValues": { ":r": recipe_name }
    }
    # Here you would call your actual AWS/DynamoDB service
    results = {"recipes": [{"food_name": recipe_name, "ingredients": ["garlic", "pasta"]}]}

    # Update state or return results
    state.output = results
    return state

# Register node with workflow
workflow.add_node("Query_search", query_search_node)

# Define AWS agent using workflow_graph
aws_agent = create_react_agent(
    name="AWSAgent",
    description="Handles AWS database queries and search workflows using workflow_graph.",
    workflow=workflow
)