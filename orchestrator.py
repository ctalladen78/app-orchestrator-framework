from agent_supervisor import AgentSupervisor

class RecipeOrchestrator:
    def __init__(self):
        self.supervisor = AgentSupervisor()

    def add_new_recipe(self, user_input, image_file=None, context=None):
        """
        Adds a new recipe: plans and executes enrichment, metadata saving, image upload.
        """
        # Assume user_input is already parsed to recipe_data
        recipe_data = user_input if isinstance(user_input, dict) else {}
        if context:
            recipe_data.update(context)

        # PLAN
        tasks = self.supervisor.plan_add_recipe(recipe_data, image_file)

        # EXECUTE
        results = self.supervisor.execute_tasks(tasks)

        # Confirm success
        if all(r.get("success", False) for r in results):
            return {"success": True, "details": results}
        else:
            return {"error": "One or more tasks failed", "details": results}

    def get_recipe(self, recipe_name):
        """
        Retrieves a recipe by name using a planned task sequence.
        """
        tasks = self.supervisor.plan_get_recipe(recipe_name)
        results = self.supervisor.execute_tasks(tasks)
        return {"success": True, "recipes": results}