import typing
from aws_cdk import aws_s3_deployment
import os
from datalake_lib.storage import uri
from pathlib import Path
from constructs import Construct

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
        self._path_to_asset = Path(path_to_asset)
        self._filename = self._path_to_asset.parts[-1]
        self._deployment_asset = aws_s3_deployment.Source.asset(
            self._path_to_asset_folder(path_to_asset),
            exclude=["**", f"!{self._path_to_asset.parts[-1]}"],
        )

    @staticmethod
    def _path_to_asset_folder(path: os.PathLike):
        path = Path(path)
        return str(Path(*list(path.parts[:-1])))

    def upload_to_bucket(
        self,
        bucket: "bucket.CdkBucket",
        object_key: os.PathLike,
        scope: typing.Optional[Construct] = None,
    ):
        scope = bucket if not scope else scope
        aws_s3_deployment.BucketDeployment(
            scope,
            self._name,
            sources=[self._deployment_asset],
            destination_bucket=bucket,
            destination_key_prefix=str(object_key),
        )
        object_key = Path(object_key) / self._filename

        return uri.S3Uri(f"{bucket.s3_url_for_object()}/{str(object_key)}")
