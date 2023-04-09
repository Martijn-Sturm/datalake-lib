import typing
from aws_cdk import aws_s3
from constructs import Construct

if typing.TYPE_CHECKING:
    from datalake_lib.storage import assets


class Bucket(typing.Protocol):
    pass
    # def add_object(self, object: "assets.Asset"):
    #     ...


class CdkBucket(aws_s3.Bucket):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)
