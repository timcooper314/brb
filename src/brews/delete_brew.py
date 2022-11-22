import os
import json
import boto3

TABLE_NAME = os.environ["BREW_RECIPES_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


def delete_dynamodb_item(brew_id: str) -> dict:
    print(f"Deleting {brew_id=} from DynamoDB table ")
    return dynamodb_table.delete_item(Key={"brewId": brew_id}, ReturnValues="ALL_OLD")


def lambda_handler(event, context):
    print(f"Request: {json.dumps(event)}")
    brew_id = event["pathParameters"]["brew"]

    deleted_brew = delete_dynamodb_item(brew_id)
    print(deleted_brew)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps({"Old brew": deleted_brew}),
    }
