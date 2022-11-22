from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct


class BrbBrewsApiStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, brew_recipes_table, inventory_table, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertools_lambda_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "PowerToolsLambdaLayer",
            layer_version_arn="arn:aws:lambda:ap-southeast-2:017000801446:layer:AWSLambdaPowertoolsPythonV2:14",
        )

        # BREWS APIs
        list_brews_function = _lambda.Function(
            self,
            "ListBrewsFunction",
            function_name=f"brb-list-brews",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="list_brews.lambda_handler",
            code=_lambda.Code.from_asset("./src/brews/"),
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
            code=_lambda.Code.from_asset("./src/brews/"),
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
            code=_lambda.Code.from_asset("./src/brews/"),
            environment=dict(
                BREW_RECIPES_TABLE_NAME=brew_recipes_table.table_name,
            ),
            timeout=Duration.seconds(10),
            layers=[powertools_lambda_layer],
        )
        brew_recipes_table.grant_write_data(create_brew_function)

        delete_brew_function = _lambda.Function(
            self,
            "DeleteBrewFunction",
            function_name="brb-delete-brew",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="delete_brew.lambda_handler",
            code=_lambda.Code.from_asset("./src/brews/"),
            environment=dict(
                BREW_RECIPES_TABLE_NAME=brew_recipes_table.table_name,
            ),
            timeout=Duration.seconds(10),
        )
        brew_recipes_table.grant_write_data(delete_brew_function)

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
        brew.add_method(
            "DELETE", apigateway.LambdaIntegration(delete_brew_function)
        )  # DELETE /brews/{brew}

        # INVENTORY APIs
        list_inventory_function = _lambda.Function(
            self,
            "ListInventoryFunction",
            function_name="brb-list-inventory",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="list_inventory.lambda_handler",
            code=_lambda.Code.from_asset("./src/inventory/"),
            environment=dict(
                INGREDIENTS_TABLE_NAME=inventory_table.table_name,
            ),
            timeout=Duration.seconds(10),
        )
        inventory_table.grant_read_data(list_inventory_function)

        update_inventory_function = _lambda.Function(
            self,
            "UpdateInventoryFunction",
            function_name=f"brb-update-inventory",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="update_inventory.lambda_handler",
            code=_lambda.Code.from_asset("./src/inventory/"),
            environment=dict(
                INGREDIENTS_TABLE_NAME=inventory_table.table_name,
            ),
            timeout=Duration.seconds(10),
            layers=[powertools_lambda_layer],
        )
        inventory_table.grant_write_data(update_inventory_function)

        inventory = brews_api.root.add_resource("inventory")
        list_inventory_integration = apigateway.LambdaIntegration(list_inventory_function)
        inventory.add_method("GET", list_inventory_integration)  # GET /inventory
        update_inventory_integration = apigateway.LambdaIntegration(update_inventory_function)
        inventory.add_method("POST", update_inventory_integration)  # POST /inventory
