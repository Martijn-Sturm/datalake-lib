import typing

if typing.TYPE_CHECKING:
    from datalake_lib.storage import uri
    from datalake_lib.storage import objects
    from datalake_lib import python


class CdkJobScript:
    def __init__(
        self,
        script_bucket_object: "objects.BucketObject",
        python_version: "python.Version",
    ) -> None:
        self._script_bucket_object = script_bucket_object
        self._python_version = python_version

    def get_script_s3_uri(self) -> "uri.S3Uri":
        return self._script_bucket_object.get_object_s3_uri()
