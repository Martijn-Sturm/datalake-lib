import typing

if typing.TYPE_CHECKING:
    from datalake_lib.storage import uri


class JobScript(typing.Protocol):
    def get_script_s3_uri(self) -> "uri.S3Uri":
        ...
