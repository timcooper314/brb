#!/usr/bin/env python3
import os
import aws_cdk as cdk
from brb_brews.brb_brews_stack import BrbBrewsStack


app = cdk.App()
BrbBrewsStack(
    app, "BrbBrewsStack",
    env=cdk.Environment(account='158795226448', region='ap-southeast-2'),
    )

app.synth()
