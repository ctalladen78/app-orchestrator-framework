
import { Api, Function, StackContext } from "sst/constructs";

export default function App({ stack }: StackContext) {
  const addRecipe = new Function(stack, "AddRecipeFunction", {
    handler: "src/addRecipe.handler",
  });

  const api = new Api(stack, "Api", {
    routes: {
      "POST /recipe": addRecipe,
      "GET /recipes": "src/getRecipes.handler",
    },
  });

  stack.addOutputs({
    ApiEndpoint: api.url,
  });
}