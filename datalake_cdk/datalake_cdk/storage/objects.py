from datalake_cdk.storage import bucket, assets
import os


class CdkBucketObject:
    def __init__(
        self,
        object: assets.CdkAsset,
        bucket: bucket.CdkBucket,
        object_key: os.PathLike,
    ) -> None:
        self._bucket = bucket
        self._object = object
        self._s3_uri = self._object.upload_to_bucket(
            bucket, object_key=object_key
        )

    def get_object_s3_uri(self):
        return self._s3_uri
