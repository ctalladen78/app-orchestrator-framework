
# App Architecture Overview

Below is a summary of the current backend architecture for the serverless cooking recipe app, presented as tables for each major component.

---

## 1. DynamoDB Table: RecipeTable

| Field          | Type    | Description                                                         |
|----------------|---------|---------------------------------------------------------------------|
| id             | string  | Primary key. Format: RECIPENAME-uuid. Unique for each recipe.       |
| title          | string  | Title of the recipe.                                                |
| food_name      | string  | Name of the food (may duplicate or supplement title).               |
| ingredients    | list    | List of ingredients.                                                |
| steps          | list    | List of preparation steps.                                          |
| description    | string  | Detailed description of the dish.                                   |
| nomenclature   | string  | Scientific or culinary naming.                                      |
| culture        | string  | Cultural origin or context.                                         |
| image_url      | string  | S3 URL to the recipe image.                                         |
| research_notes | string  | Additional notes (from LLM/web research enrichment).                |

**Description:**  
A single-table schema stores all recipe metadata. The primary key `id` is unique per recipe, combining the recipe name for human readability and a UUID for uniqueness.

---

## 2. S3 Bucket: RecipeImagesBucket

| Field       | Type    | Description                                  |
|-------------|---------|----------------------------------------------|
| image files | object  | Stores recipe images, referenced by image_url|
| image_url   | string  | Public or signed URL to access the image     |

**Description:**  
Used for storing images uploaded for recipes. Images are referenced by their S3 URL in the DynamoDB table.

---

## 3. Lambda Functions

| Name                   | Handler Path          | Purpose                                                  | Environment Variables                       | Permissions                          |
|------------------------|----------------------|----------------------------------------------------------|---------------------------------------------|--------------------------------------|
| AddRecipeFunction      | src/addRecipe.handler| Handles POST requests to add new recipes.                | RECIPE_TABLE_NAME, RECIPE_IMAGES_BUCKET     | Access RecipeTable and RecipeImagesBucket |
| GetRecipesFunction     | src/getRecipes.handler| Handles GET requests to retrieve known recipes.          | RECIPE_TABLE_NAME, RECIPE_IMAGES_BUCKET     | Access RecipeTable and RecipeImagesBucket |

**Description:**  
Each function is attached to an API Gateway route, receives API requests, performs validation, and interacts with DynamoDB and S3.

---

## 4. API Gateway (SST Api Layer)

| Route         | Method | Lambda Function      | Description                        |
|---------------|--------|---------------------|-------------------------------------|
| /recipe       | POST   | AddRecipeFunction   | Add a new recipe                    |
| /recipes      | GET    | GetRecipesFunction  | Retrieve recipes (optionally filter)|

**Description:**  
API Gateway exposes HTTP endpoints for client interaction, routing requests to the appropriate Lambda functions.

---

## 5. LLM Integration (OpenAI via llm_interface component)

| Function                       | Purpose                                      |
|--------------------------------|----------------------------------------------|
| detect_intent                  | Extracts user intent and recipe data         |
| enrich_recipe_with_web_research| Enriches recipe with web-sourced context     |
| format_recipe_list             | Formats recipe data for API responses        |

**Description:**  
Used for advanced parsing, enrichment, and formatting of recipe data during add and query flows.

---

## 6. Web Research Agent (LangChain)

| Component                | Description                                                                       |
|--------------------------|-----------------------------------------------------------------------------------|
| web_research_agent.py    | LangChain-powered agent that uses web search (DuckDuckGo) and LLM for enrichment |
| DuckDuckGoSearchRun      | Tool for searching recipe context, ingredients, origin, etc.                      |
| PromptTemplate           | Guides the agent to merge web research with app recipe data                       |
| OpenAI LLM               | Generates enriched recipe fields and research notes                               |

**Description:**  
The agent is invoked during the add recipe workflow. It performs web searches for recipes, merges the results with user-provided data, and returns a comprehensive, enriched recipe object. This ensures recipes contain accurate, complete, and culturally contextual information.

---

## Summary Diagram

- **Client** → **API Gateway** → **Lambda Functions** → **DynamoDB (RecipeTable) & S3 (RecipeImagesBucket)**
- **LLM Interface** and **Web Research Agent** are invoked within Lambda for intent detection, data enrichment, and formatting.

```