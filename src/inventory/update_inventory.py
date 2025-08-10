import os
import json
from typing import List
import boto3
from aws_lambda_powertools.utilities.parser import (
    BaseModel,
    event_parser,
    envelopes,
)

TABLE_NAME = os.environ["INGREDIENTS_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


class Ingredient(BaseModel):
    ingredient: str
    type: str  # grain, hops, yeast or other
    quantity: int  # grams


class Inventory(BaseModel):
    inventory: List[Ingredient]


def put_dynamodb_item(ingredient: Ingredient) -> dict:
    print(f"Putting brew {ingredient.ingredient} into DynamoDB table")
    return dynamodb_table.put_item(Item=ingredient.dict())


# @event_parser(model=Ingredient, envelope=envelopes.ApiGatewayEnvelope)
def lambda_handler(event, context):
    print(f"Request: {event}")
    event_body = json.loads(event["body"])
    updated_ingredient = Ingredient(**event_body)
    response = put_dynamodb_item(updated_ingredient)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps({"Updated Ingredient": updated_ingredient.dict()}),
    }
