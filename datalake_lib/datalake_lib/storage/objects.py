import typing

if typing.TYPE_CHECKING:
    from datalake_lib.storage import uri


class BucketObject(typing.Protocol):
    def get_object_s3_uri(self) -> "uri.S3Uri":
        ...
