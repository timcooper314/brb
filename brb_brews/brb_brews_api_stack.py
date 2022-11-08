from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct


class BrbBrewsApiStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, brew_recipes_table, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        list_brews_function = _lambda.Function(
            self,
            "ListBrewsFunction",
            function_name=f"brb-list-brews",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="list_brews.lambda_handler",
            code=_lambda.Code.from_asset("./src/"),
            environment=dict(
                BREW_RECIPES_TABLE_NAME=brew_recipes_table.table_name,
            ),
            timeout=Duration.seconds(10),
        )
        brew_recipes_table.grant_read_data(list_brews_function)

        get_brew_function = _lambda.Function(
            self,
            "GetBrewFunction",
            function_name=f"brb-get-brew",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="get_brew.lambda_handler",
            code=_lambda.Code.from_asset("./src/"),
            environment=dict(
                BREW_RECIPES_TABLE_NAME=brew_recipes_table.table_name,
            ),
            timeout=Duration.seconds(10),
        )
        brew_recipes_table.grant_read_data(get_brew_function)

        create_brew_function = _lambda.Function(
            self,
            "CreateBrewFunction",
            function_name=f"brb-create-brew",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="create_brew.lambda_handler",
            code=_lambda.Code.from_asset("./src/"),
            environment=dict(
                BREW_RECIPES_TABLE_NAME=brew_recipes_table.table_name,
            ),
            timeout=Duration.seconds(10),
        )
        brew_recipes_table.grant_write_data(create_brew_function)

        brews_api = apigateway.LambdaRestApi(
            self,
            "BrewsRestAPI",
            handler=list_brews_function,
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_headers=apigateway.Cors.ALL_ORIGINS,
            ),
        )
        brews = brews_api.root.add_resource("brews")
        brews.add_method("GET")  # GET /brews
        create_brew_integration = apigateway.LambdaIntegration(create_brew_function)
        brews.add_method("POST", create_brew_integration)  # POST /brews

        brew = brews.add_resource("{brew}")
        brew.add_method(
            "GET", apigateway.LambdaIntegration(get_brew_function)
        )  # GET /brews/{brew}
