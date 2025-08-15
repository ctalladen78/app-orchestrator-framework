from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

aws_agent = create_react_agent(name="AWSAgent")
web_research_agent = create_react_agent(name="WebResearchAgent")

agent_supervisor = create_supervisor(
    agents={
        "aws": aws_agent,
        "web_research": web_research_agent
    }
)

def detect_intent(user_input):
    """
    Naive example: determines intent to 'make_new_recipe' or 'get_recipes' based on user_input.
    Replace with LLM or NLP for production.
    """
    text = str(user_input).lower()
    if any(kw in text for kw in ["add", "make", "create", "new recipe"]):
        return "make_new_recipe"
    if any(kw in text for kw in ["get", "find", "show", "see", "retrieve", "lookup", "search", "list"]):
        return "get_recipes"
    return "unknown"

class AgentSupervisor:
    """
    Determines intent and delegates to agents for the correct workflow.
    """
    def handle_user_request(self, user_input, image_file=None, context=None):
        intent = detect_intent(user_input)
        
        if intent == "make_new_recipe":
            recipe_data = user_input if isinstance(user_input, dict) else {}
            if context:
                recipe_data.update(context)
            tasks = [
                {"agent": "web_research", "action": "enrich_recipe", "payload": recipe_data},
                {"agent": "aws", "action": "PutItem", "resource": "DynamoDB", "payload": recipe_data}
            ]
            if image_file:
                tasks.append({
                    "agent": "aws",
                    "action": "UploadFile",
                    "resource": "S3",
                    "payload": {"file": image_file, "recipe_name": recipe_data.get("food_name", recipe_data.get("title"))}
                })
            results = [agent_supervisor.run(**task) for task in tasks]
            return {"intent": intent, "results": results}

        elif intent == "get_recipes":
            # For simplicity, assume user_input is recipe name or query
            recipe_name = user_input if isinstance(user_input, str) else user_input.get("food_name", "")
            tasks = [
                {
                    "agent": "aws",
                    "action": "Query",
                    "resource": "DynamoDB",
                    "payload": {
                        "KeyConditionExpression": "food_name = :r",
                        "ExpressionValues": {":r": recipe_name}
                    }
                }
            ]
            results = [agent_supervisor.run(**task) for task in tasks]
            return {"intent": intent, "results": results}
        
        else:
            return {"intent": "unknown", "error": "Intent not recognized."}