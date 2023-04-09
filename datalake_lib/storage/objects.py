import typing
from datalake_lib.storage import bucket, assets
import os

if typing.TYPE_CHECKING:
    from datalake_lib.storage import uri


class BucketObject:
    def __init__(
        self, object: assets.Asset, bucket: bucket.Bucket, object_key: os.PathLike
    ) -> None:
        self._bucket = bucket
        self._object = object
        self._s3_uri = self._object.upload_to_bucket(bucket, object_key=object_key)

    def get_object_s3_uri(self):
        return self._s3_uri
