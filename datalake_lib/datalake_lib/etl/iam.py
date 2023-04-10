import typing
import os
import dataclasses


class Role(typing.Protocol):
    def get_arn(self) -> str:
        ...


@dataclasses.dataclass
class BucketAccessConfiguration:
    bucket_arn: str
    bucket_paths: typing.Optional[typing.Sequence[os.PathLike]] = None
