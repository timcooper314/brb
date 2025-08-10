import os
import json
from decimal import Decimal
import boto3


TABLE_NAME = os.environ["INGREDIENTS_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def scan_dynamodb() -> list:
    print(f"Scanning all items in dynamodb table {TABLE_NAME}")
    response = dynamodb_table.scan()
    return response["Items"]


def lambda_handler(event, context):
    print(f"Request: {json.dumps(event)}")
    inventory_list = scan_dynamodb()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps({"inventory": inventory_list}, cls=DecimalEncoder),
    }
