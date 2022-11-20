from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct


class BrbBrewsFrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        site_bucket = s3.Bucket(
            self,
            "FrontendBucket",
            bucket_name="brb-brews-frontend",
            website_index_document="index.html",
            # block_public_access=s3.BlockPublicAccess.
        )
        site_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[f"{site_bucket.bucket_arn}/*"],
                principals=[iam.AnyPrincipal()],
            )
        )
