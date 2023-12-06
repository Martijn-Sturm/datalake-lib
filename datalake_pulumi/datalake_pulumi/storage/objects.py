from datalake_pulumi.storage import assets
from pulumi_aws import s3
import os


class PulumiBucketObject:
    def __init__(
        self,
        object: assets.PulumiAsset,
        bucket: s3.Bucket,
        object_key: os.PathLike,
    ) -> None:
        self._bucket = bucket
        self._object = object
        self._s3_uri = self._object.upload_to_bucket(
            bucket, object_key=object_key
        )

    def get_object_s3_uri(self):
        return self._s3_uri
