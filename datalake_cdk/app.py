#!/usr/bin/env python3
from pathlib import Path
import aws_cdk as cdk
from datalake_cdk.storage import bucket, objects, assets
from datalake_cdk.etl import job, script, iam
from datalake_lib.etl import arguments, options
from datalake_lib.etl.iam import BucketAccessConfiguration
from datalake_lib.etl.job import JobProperties
from datalake_lib import python

move_to_repo_root_path = Path("..")


class DatalakeStack(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        glue_bucket = bucket.CdkBucket(self, "glue-assets")

        local_lib_wheel_path = (
            move_to_repo_root_path
            / "libs/demo_lib/dist/demo_lib-0.1.0-py3-none-any.whl"
        )
        demo_lib = objects.CdkBucketObject(
            assets.CdkAsset(
                str(move_to_repo_root_path / "demo_lib"), local_lib_wheel_path
            ),
            bucket=glue_bucket,
            object_key=Path("wheels"),
        )

        job_script_path = (
            move_to_repo_root_path / "glue_job_scripts/demo_script.py"
        )
        job_script_file = objects.CdkBucketObject(
            assets.CdkAsset(
                str(move_to_repo_root_path / "job_script"), job_script_path
            ),
            bucket=glue_bucket,
            object_key=Path("scripts"),
        )
        job_script = script.CdkJobScript(
            job_script_file, python.Version.PYTHON3_10
        )

        glue_role = iam.CdkGlueJobRole(
            self,
            "glue",
            bucket_read_access_configurations=[
                BucketAccessConfiguration(glue_bucket.bucket_arn)
            ],
            bucket_write_access_configurations=[
                BucketAccessConfiguration(
                    glue_bucket.bucket_arn,
                )
            ],
        )
        job_args = [
            arguments.CustomDefaultArgument("demo_argument", "demo_value"),
            arguments.DatalakeFormatArgument([options.DatalakeFormat.HUDI]),
            arguments.EnableContinuousCloudwatchLog(
                enable=True, filter_apache_logs=True
            ),
            arguments.EnableGlueCatalog(True),
            arguments.PythonPackageDependencies(
                pip_installable_packages=[
                    arguments.PipInstallablePackage(
                        "glue-helper-lib",
                        version_specifier=arguments.VersionSpecifier.MATCH,
                        version_value="0.1.0",
                    )
                ],
                s3_python_wheels=[demo_lib.get_object_s3_uri()],
            ),
        ]

        job.Job(
            self,
            "etl",
            JobProperties(
                script=job_script,
                iam_role=glue_role,
                max_retries=0,
                default_arguments=job_args,
            ),
        )


app = cdk.App()
DatalakeStack(
    app,
    "DatalakeStack",
    env=cdk.Environment(region="eu-central-1"),
)

app.synth()
