from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class BrbBrewsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        brew_recipes_table = dynamodb.Table(
            self,
            "BrewRecipesTable",
            table_name="BRBBrewRecipes",
            partition_key=dynamodb.Attribute(
                name="brewId", type=dynamodb.AttributeType.STRING
            ),
        )
