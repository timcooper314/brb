import os
import json
from datetime import datetime
import boto3

TABLE_NAME = os.environ["BREW_RECIPES_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


# TODO: Dataclass for Brew


def put_dynamodb_item(brew: dict) -> dict:
    print(f"Putting brew {brew['brewId']} into DynamoDB table")
    return dynamodb_table.put_item(Item=brew)


def lambda_handler(event, context):
    print(f"Request: {json.dumps(event)}")
    new_brew = json.loads(event["body"])
    if not new_brew.get("brewId"):  # Fresh brew!
        new_brew["brewId"] = datetime.now().strftime("%Y%m%d%H%M%S")
    brew = put_dynamodb_item(new_brew)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"New brew": new_brew}),
    }
