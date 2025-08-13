import { ApiHandler } from "sst/node/api";
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
import { v4 as uuidv4 } from "uuid";

const client = new DynamoDBClient({});
const TABLE_NAME = process.env.RECIPE_TABLE_NAME!;

export const handler = ApiHandler(async (event) => {
  let body: any;
  try {
    body = typeof event.body === "string" ? JSON.parse(event.body) : event.body;
  } catch {
    body = event.body;
  }

  const { title, food_name, ingredients, steps, description, nomenclature, culture, image_url, research_notes } = body;

  if (!food_name && !title) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "food_name or title is required" }),
    };
  }
  if (!ingredients || !Array.isArray(ingredients) || ingredients.length === 0) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "ingredients must be a non-empty array" }),
    };
  }
  if (!steps || !Array.isArray(steps) || steps.length === 0) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "steps must be a non-empty array" }),
    };
  }

  const namePart = (food_name || title).replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
  const recipe_id = `${namePart}-${uuidv4()}`;

  const item: any = {
    id: { S: recipe_id },
    title: title ? { S: title } : undefined,
    food_name: food_name ? { S: food_name } : undefined,
    ingredients: { L: ingredients.map((i: string) => ({ S: i })) },
    steps: { L: steps.map((i: string) => ({ S: i })) },
    description: description ? { S: description } : undefined,
    nomenclature: nomenclature ? { S: nomenclature } : undefined,
    culture: culture ? { S: culture } : undefined,
    image_url: image_url ? { S: image_url } : undefined,
    research_notes: research_notes ? { S: research_notes } : undefined,
  };
  Object.keys(item).forEach((key) => item[key] === undefined && delete item[key]);

  try {
    await client.send(
      new PutItemCommand({
        TableName: TABLE_NAME,
        Item: item,
      })
    );
    return {
      statusCode: 201,
      body: JSON.stringify({ success: true, recipe_id }),
    };
  } catch (err: any) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message }),
    };
  }
});