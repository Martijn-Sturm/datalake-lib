from aws_cdk import aws_glue
from constructs import Construct
import typing

if typing.TYPE_CHECKING:
    from datalake_lib.etl import security


class CDKSecurityConfiguration(Construct):
    sec_config_id = "sec-config"

    def __init__(
        self,
        scope: Construct,
        id: str,
        properties: "security.SecurityConfigurationProperties",
    ) -> None:
        super().__init__(scope, id)
        self._name = f"{id}-{self.sec_config_id}"
        aws_glue.CfnSecurityConfiguration(
            self,
            f"{id}-{self.sec_config_id}",
            encryption_configuration=aws_glue.CfnSecurityConfiguration.EncryptionConfigurationProperty(
                cloud_watch_encryption=aws_glue.CfnSecurityConfiguration.CloudWatchEncryptionProperty(
                    cloud_watch_encryption_mode="SSE-KMS",
                    kms_key_arn=properties.cloudwatch_kms_key_arn,
                ),
                job_bookmarks_encryption=aws_glue.CfnSecurityConfiguration.JobBookmarksEncryptionProperty(
                    job_bookmarks_encryption_mode="SSE-KMS",
                    kms_key_arn=properties.jobbookmark_kms_key_arn,
                ),
                s3_encryptions=[
                    aws_glue.CfnSecurityConfiguration.S3EncryptionProperty(
                        s3_encryption_mode="SSE-KMS",
                        kms_key_arn=properties.s3_encryption_kms_key_arn,
                    )
                ],
            ),
            name=self._name,
        )

    def get_name(self):
        return self._name
