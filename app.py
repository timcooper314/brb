#!/usr/bin/env python3
import os
import aws_cdk as cdk
from brb_brews.storage_stack import BrbBrewsStorageStack
from brb_brews.api_stack import BrbBrewsApiStack
from brb_brews.frontend_stack import BrbBrewsFrontendStack


app = cdk.App()
cdk_env = cdk.Environment(account="158795226448", region="ap-southeast-2")

storage = BrbBrewsStorageStack(
    app,
    "BrbBrewsStorageStack",
    env=cdk_env,
)
api = BrbBrewsApiStack(
    app,
    "BrbBrewsApiStack",
    env=cdk_env,
    brew_recipes_table=storage.brew_recipes_table,
)
frontend = BrbBrewsFrontendStack(
    app,
    "BrbBrewsFrontendStack",
    env=cdk_env,
)

app.synth()
