from pulumi_aws import iam as pulumi_iam
import typing
import os
from datalake_lib.etl import iam


class PulumiGlueJobRole(iam.Role):
    def __init__(
        self,
        id: str,
        bucket_read_access_configurations: typing.Sequence[
            iam.BucketAccessConfiguration
        ],
        bucket_write_access_configurations: typing.Sequence[
            iam.BucketAccessConfiguration
        ],
        *,
        description=None,
        external_ids=None,
        inline_policies=None,
        managed_policies=None,
        role_name: typing.Optional[str] = None,
    ) -> None:
        self._role = pulumi_iam.Role(f"{id}-glue-role")
        if managed_policies:
            for policy in managed_policies:
                self.add_managed_policy(policy)

        for config in bucket_read_access_configurations:
            self.attach_inline_policy(
                self._generate_bucket_read_policy(
                    config.bucket_arn, config.bucket_paths
                )
            )
        for config in bucket_write_access_configurations:
            self.attach_inline_policy(
                self._generate_bucket_write_policy(
                    config.bucket_arn, config.bucket_paths
                )
            )

    def get_arn(self):
        return self.role_arn

    @staticmethod
    def _generate_bucket_read_policy_statements(
        bucket_arn: str,
        paths_in_bucket: typing.Optional[typing.Sequence[os.PathLike]],
    ):
        return [
            aws_iam.PolicyStatement(
                actions=["s3:ListBucket"],
                effect=aws_iam.Effect.ALLOW,
                resources=[bucket_arn]
                if not paths_in_bucket
                else [f"{bucket_arn}/{path}" for path in paths_in_bucket],
            ),
            aws_iam.PolicyStatement(
                actions=["s3:GetObject"],
                effect=aws_iam.Effect.ALLOW,
                resources=[f"{bucket_arn}/*"]
                if not paths_in_bucket
                else [f"{bucket_arn}/{path}/*" for path in paths_in_bucket],
            ),
        ]

    def _generate_bucket_read_policy(
        self,
        bucket_arn: str,
        paths_in_bucket: typing.Optional[typing.Sequence[os.PathLike]],
    ):
        return aws_iam.Policy(
            self._scope,
            "bucket-read",
            document=aws_iam.PolicyDocument(
                statements=self._generate_bucket_read_policy_statements(
                    bucket_arn, paths_in_bucket
                )
            ),
        )

    def _generate_bucket_write_policy(
        self,
        bucket_arn: str,
        paths_in_bucket: typing.Optional[typing.Sequence[os.PathLike]],
    ):
        return aws_iam.Policy(
            self._scope,
            "bucket-write",
            document=aws_iam.PolicyDocument(
                statements=[
                    *self._generate_bucket_read_policy_statements(
                        bucket_arn, paths_in_bucket
                    ),
                    aws_iam.PolicyStatement(
                        actions=["s3:PutObject", "s3:DeleteObject"],
                        effect=aws_iam.Effect.ALLOW,
                        resources=[f"{bucket_arn}/*"]
                        if not paths_in_bucket
                        else [
                            f"{bucket_arn}/{path}/*"
                            for path in paths_in_bucket
                        ],
                    ),
                ]
            ),
        )
