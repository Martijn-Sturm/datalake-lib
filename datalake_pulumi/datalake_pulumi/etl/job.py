import typing
from constructs import Construct
from datalake_lib.etl import options
from aws_cdk import aws_glue

if typing.TYPE_CHECKING:
    from datalake_lib.etl import arguments, job


class Job(Construct):
    def __init__(
        self, scope: Construct, id: str, properties: "job.JobProperties"
    ):
        self._id = id
        super().__init__(scope, id)
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html
        self._commands_properties = aws_glue.CfnJob.JobCommandProperty(
            name=options.JobType.GLUE_ETL.value,
            script_location=str(properties.script.get_script_s3_uri()),
        )
        aws_glue.CfnJob(
            self,
            id,
            command=self._commands_properties,
            default_arguments=self._get_default_arguments_as_dict(
                properties.default_arguments
            ),
            role=properties.iam_role.get_arn(),
            glue_version=properties.glue_version.value,
            max_capacity=properties.max_number_of_workers,
            max_retries=properties.max_retries,
            execution_class=properties.execution_class.value,
            number_of_workers=properties.number_of_workers,
            worker_type=properties.worker_type.value,
            timeout=properties.timeout_minutes,
            security_configuration=properties.security_configuration.get_name()
            if properties.security_configuration
            else None,
        )

    @staticmethod
    def _get_default_arguments_as_dict(
        default_arguments: typing.Sequence["arguments.DefaultArgument"],
    ):
        result = {}
        for default_argument in default_arguments:
            result.update(default_argument.get_dict_representation())
        return result
