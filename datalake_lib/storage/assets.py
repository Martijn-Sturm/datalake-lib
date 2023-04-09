import typing
from aws_cdk import aws_s3_deployment
import os
from constructs import Construct
from datalake_lib.storage import uri

if typing.TYPE_CHECKING:
    from datalake_lib.storage import bucket


class Asset(typing.Protocol):
    def upload_to_bucket(
        self, bucket: "bucket.Bucket", object_key: os.PathLike
    ) -> uri.S3Uri:
        ...


class CdkAsset(Asset):
    def __init__(self, asset_name: str, path_to_asset: os.PathLike) -> None:
        self._name = asset_name
        self._path_to_asset = path_to_asset
        self._deployment_asset = aws_s3_deployment.Source.asset(
            str(self._path_to_asset)
        )

    def upload_to_bucket(
        self,
        bucket: "bucket.CdkBucket",
        object_key: os.PathLike,
        scope: typing.Optional[Construct] = None,
    ):
        scope = bucket if not scope else scope
        object = aws_s3_deployment.BucketDeployment(
            scope,
            self._name,
            sources=[self._deployment_asset],
            destination_bucket=bucket,
            destination_key_prefix=str(object_key),
        )
        s3_uri = uri.S3Uri(object.object_keys[0])
        return s3_uri
