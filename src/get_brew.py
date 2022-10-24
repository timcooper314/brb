import os
import json
import boto3

TABLE_NAME = os.environ["BREW_RECIPES_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


def get_dynamodb_item(brew_id: str) -> dict:
    print(f"Retrieving {brew_id=} from DynamoDB table ")
    return dynamodb_table.get_item(Key={"brewId": brew_id})["Item"]


def lambda_handler(event, context):
    print(f"Request: {json.dumps(event)}")
    brew_id = event["pathParameters"]["brew"]

    brew = get_dynamodb_item(brew_id)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(brew),
    }
