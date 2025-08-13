
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate

# Define a tool for web search
search = DuckDuckGoSearchRun()

# Prompt template for recipe enrichment
enrichment_prompt = PromptTemplate(
    input_variables=["recipe", "research"],
    template=(
        "Given the following recipe data:\n{recipe}\n"
        "And these web research results:\n{research}\n"
        "Enrich the recipe with missing details (ingredients, steps, culture, nomenclature, description) "
        "and provide a concise research_notes summary. Return a JSON object with all fields."
    )
)

def enrich_recipe_with_web_research(recipe_data: dict) -> dict:
    """
    Uses LangChain to perform web search and enrich recipe data.
    """
    llm = OpenAI(temperature=0.7)  # You may use ChatOpenAI for GPT-4
    agent_tools = [
        Tool(
            name="Web Search",
            func=search.run,
            description="Useful for finding up-to-date recipe information and context."
        ),
    ]
    # Initialize a zero-shot agent with web search capability
    agent = initialize_agent(
        agent_tools,
        llm,
        agent="zero-shot-react-description",
        verbose=False,
    )

    # Step 1: Perform web search for this recipe
    query = f"{recipe_data.get('food_name', recipe_data.get('title', ''))} recipe origin ingredients steps"
    research_results = agent.run(query)

    # Step 2: Use LLM to merge and enrich
    prompt = enrichment_prompt.format(
        recipe=str(recipe_data),
        research=research_results
    )
    enriched_text = llm(prompt)

    # Step 3: Parse JSON output (assume LLM returns valid JSON)
    import json
    try:
        enriched_recipe = json.loads(enriched_text)
    except Exception:
        enriched_recipe = recipe_data.copy()
        enriched_recipe["research_notes"] = research_results
    return enriched_recipe