import dataclasses
import typing


@dataclasses.dataclass
class SecurityConfigurationProperties:
    cloudwatch_kms_key_arn: str
    jobbookmark_kms_key_arn: str
    s3_encryption_kms_key_arn: str


class SecurityConfiguration(typing.Protocol):
    def get_name(self) -> str:
        ...
