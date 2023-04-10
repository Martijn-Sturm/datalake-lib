import typing
from datalake_lib.etl import script, iam, options
from datalake_lib import python
import dataclasses
import enum

if typing.TYPE_CHECKING:
    from datalake_lib.storage import uri
    from datalake_lib.etl import arguments, security


class GlueVersion(enum.Enum):
    V4_0 = "4.0"
    V3_0 = "3.0"


@dataclasses.dataclass
class ScriptDeploymentProperties:
    script_location: "uri.S3Uri"
    python_version: "python.Version"
    job_type: options.JobType = options.JobType.GLUE_ETL


@dataclasses.dataclass
class JobProperties:
    script: script.JobScript
    iam_role: iam.Role
    default_arguments: typing.Sequence["arguments.DefaultArgument"]
    security_configuration: typing.Optional[
        "security.SecurityConfiguration"
    ] = None
    worker_type: options.WorkerType = options.WorkerType.G_1X
    timeout_minutes: int = 60
    number_of_workers: int = 2
    max_number_of_workers: typing.Optional[int] = None
    glue_version: GlueVersion = GlueVersion.V4_0
    max_retries: int = 1
    execution_class: options.ExecutionClass = options.ExecutionClass.STANDARD
