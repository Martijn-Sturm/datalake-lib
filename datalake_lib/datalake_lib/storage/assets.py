import typing
import os
from datalake_lib.storage import uri

if typing.TYPE_CHECKING:
    from datalake_lib.storage import bucket


class Asset(typing.Protocol):
    def upload_to_bucket(
        self, bucket: "bucket.Bucket", object_key: os.PathLike
    ) -> uri.S3Uri:
        ...
