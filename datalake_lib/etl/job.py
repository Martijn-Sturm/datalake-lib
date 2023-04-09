import typing
from constructs import Construct
from datalake_lib.etl import script, iam
import dataclasses
from aws_cdk import aws_glue
import enum

if typing.TYPE_CHECKING:
    from datalake_lib import python
    from datalake_lib.storage import uri
    from datalake_lib.etl import arguments


class GlueVersion(enum.Enum):
    V4_0 = "4.0"
    V3_0 = "3.0"


class WorkerType(enum.Enum):
    G_1X = "G.1X"
    G_2X = "G.2X"


class JobType(enum.Enum):
    GLUE_ETL = "glueetl"
    PYTHON_SHELL = "pythonshell"


@dataclasses.dataclass
class ScriptDeploymentProperties:
    script_location: "uri.S3Uri"
    python_version: "python.Version"
    job_type: JobType = JobType.GLUE_ETL


@dataclasses.dataclass
class JobProperties:
    script: script.Script
    glue_version: GlueVersion
    max_number_of_workers: int
    worker_type: WorkerType
    max_retries: int
    timeout_minutes: int
    iam_role: iam.Role
    default_arguments: typing.Sequence[arguments.DefaultArgument]
    max_retries: int = 1


class Job(Construct):
    def __init__(self, scope: Construct, id: str, properties: JobProperties) -> None:
        super().__init__(scope, id)
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html
        self._commands_properties = aws_glue.CfnJob.JobCommandProperty(
            name=JobType.GLUE_ETL.value,
            python_version=python.Version.PYTHON3_10.value,
            script_location=str(properties.script.get_script_s3_uri()),
        )
        aws_glue.CfnJob(
            self,
            id,
            command=self._commands_properties,
            role=properties.iam_role.get_arn(),
            glue_version=properties.glue_version.value,
            max_capacity=properties.max_number_of_workers,
            default_arguments=[],
            max_retries=properties.max_retries,
        )
