
import { ApiHandler } from "sst/node/api";
import { DynamoDBClient, ScanCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});
const TABLE_NAME = process.env.RECIPE_TABLE_NAME!;

export const handler = ApiHandler(async (event) => {
  const params = event.queryStringParameters || {};
  const ingredientFilter = params.ingredient;

  let scanInput: any = {
    TableName: TABLE_NAME,
  };

  if (ingredientFilter) {
    scanInput.FilterExpression = "contains(ingredients, :ingredientVal)";
    scanInput.ExpressionAttributeValues = {
      ":ingredientVal": { S: ingredientFilter },
    };
  }

  try {
    const resp = await client.send(new ScanCommand(scanInput));
    const recipes = (resp.Items || []).map((item: any) => ({
      id: item.id?.S,
      title: item.title?.S,
      food_name: item.food_name?.S,
      ingredients: item.ingredients?.L?.map((i: any) => i.S) ?? [],
      steps: item.steps?.L?.map((i: any) => i.S) ?? [],
      description: item.description?.S,
      nomenclature: item.nomenclature?.S,
      culture: item.culture?.S,
      image_url: item.image_url?.S,
      research_notes: item.research_notes?.S,
    }));

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, recipes }),
    };
  } catch (err: any) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message }),
    };
  }
});