import os
import json
from datetime import datetime
from typing import Optional
import boto3
from aws_lambda_powertools.utilities.parser import (
    BaseModel,
    Field,
    event_parser,
    envelopes,
)

TABLE_NAME = os.environ["BREW_RECIPES_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(TABLE_NAME)


def create_date_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")


class Brew(BaseModel):
    brewId: str = Field(default_factory=create_date_id)
    name: str
    brewDate: Optional[str] = Field
    hops: Optional[str]
    grain: Optional[str]
    yeast: Optional[str]


def put_dynamodb_item(brew: Brew) -> dict:
    print(f"Putting brew {brew.name} into DynamoDB table")
    return dynamodb_table.put_item(Item=brew.dict())


@event_parser(model=Brew, envelope=envelopes.ApiGatewayEnvelope)
def lambda_handler(event: Brew, context):
    print(f"Request: {event}")
    new_brew = event
    response = put_dynamodb_item(new_brew)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps({"New brew": new_brew.dict()}),
    }
