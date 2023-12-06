import os
from datalake_lib.storage import uri
from pathlib import Path
import pulumi
from pulumi_aws import s3


class PulumiAsset:
    def __init__(self, asset_name: str, path_to_asset: os.PathLike) -> None:
        self._name = asset_name
        self._path_to_asset = Path(path_to_asset)
        self._filename = self._path_to_asset.parts[-1]
        self._deployment_asset = pulumi.FileAsset(path_to_asset)

    def upload_to_bucket(
        self,
        bucket: "s3.Bucket",
        object_key: os.PathLike,
    ):
        bucket_name = bucket.bucket
        s3.BucketObject(
            resource_name=self._name,
            source=self._deployment_asset,
            bucket=bucket_name,
            key=str(object_key),
        )
        object_key = Path(object_key) / self._filename

        return uri.S3Uri(f"s3://{bucket_name}/{str(object_key)}")
