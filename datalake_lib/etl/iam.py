from aws_cdk import aws_iam
from constructs import Construct
import typing
import os
import dataclasses


class Role(typing.Protocol):
    def get_arn(self) -> str:
        ...


@dataclasses.dataclass
class BucketAccessConfiguration:
    bucket_arn: str
    bucket_paths: typing.Optional[typing.Sequence[os.PathLike]]


class CdkGlueJobRole(aws_iam.Role):
    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket_read_access_configurations: typing.Sequence[BucketAccessConfiguration],
        bucket_write_access_configurations: typing.Sequence[BucketAccessConfiguration],
        *,
        description=None,
        external_ids=None,
        inline_policies=None,
        managed_policies=None,
        role_name: typing.Optional[str] = None,
    ) -> None:
        self._scope = scope
        super().__init__(
            scope,
            id,
            assumed_by=aws_iam.ServicePrincipal("glue"),
            description=description,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=[
                aws_iam.ManagedPolicy.from_managed_policy_arn(
                    scope,
                    id="servicerole",
                    managed_policy_arn="arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole",
                )
            ],
            role_name=role_name,
        )
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
                        else [f"{bucket_arn}/{path}/*" for path in paths_in_bucket],
                    ),
                ]
            ),
        )
