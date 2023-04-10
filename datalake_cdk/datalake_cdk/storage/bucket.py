from aws_cdk import aws_s3, RemovalPolicy
from constructs import Construct


class CdkBucket(aws_s3.Bucket):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id, removal_policy=RemovalPolicy.DESTROY)
