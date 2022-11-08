import os
import json
import boto3


TABLE_NAME = os.environ["BREW_RECIPES_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


def scan_dynamodb() -> list:
    print(f"Scanning all items in dynamodb table {TABLE_NAME}")
    response = dynamodb_table.scan()
    return response["Items"]


def lambda_handler(event, context):
    print(f"Request: {json.dumps(event)}")
    brew_list = scan_dynamodb()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps({"brews": brew_list}),
    }
