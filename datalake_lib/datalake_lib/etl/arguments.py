import typing
import dataclasses
import enum

if typing.TYPE_CHECKING:
    from datalake_lib.etl import options
    from datalake_lib.storage import uri


# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html


def process_arg_name(name: str):
    return f"--{name}"


class DefaultArgument(typing.Protocol):
    def get_dict_representation(self) -> typing.Dict[str, str]:
        ...


class ScriptLocation(DefaultArgument):
    def __init__(self, script_location: "uri.S3Uri") -> None:
        self._script_s3_uri = str(script_location)

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {process_arg_name("script-location"): self._script_s3_uri}


class CustomDefaultArgument(DefaultArgument):
    def __init__(self, name: str, value: str) -> None:
        self._name = name
        self._value = value

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {process_arg_name(self._name): self._value}


class DatalakeFormatArgument:
    def __init__(
        self,
        datalake_formats: typing.Sequence["options.DatalakeFormat"],
    ) -> None:
        self._formats: typing.Sequence[str] = [
            format.value for format in datalake_formats
        ]

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {"--datalake-formats": ",".join(self._formats)}


class VersionSpecifier(enum.Enum):
    # https://peps.python.org/pep-0440/#version-specifiers
    COMPATIBLE = "~="
    MATCH = "=="
    GREATER_THAN = ">="
    SMALLER_THAN = "<="


@dataclasses.dataclass
class PipInstallablePackage:
    package_name: str
    version_specifier: typing.Optional[VersionSpecifier] = None
    version_value: typing.Optional[str] = None


class PythonPackageDependencies(DefaultArgument):
    def __init__(
        self,
        pip_installable_packages: typing.Optional[
            typing.Sequence[PipInstallablePackage]
        ] = None,
        s3_python_wheels: typing.Optional[typing.Sequence["uri.S3Uri"]] = None,
    ) -> None:
        self._pip_installable_packages = (
            pip_installable_packages if pip_installable_packages else []
        )
        self._s3_python_wheels = (
            [str(uri) for uri in s3_python_wheels] if s3_python_wheels else []
        )

    @staticmethod
    def _get_specification_for_pip_package(
        package: PipInstallablePackage,
    ) -> str:
        if package.version_value:
            if package.version_specifier:
                return (
                    f"{package.package_name}{package.version_specifier.value}"
                    f"{package.version_value}"
                )
            else:
                return f"{package.package_name}=={package.version_value}"
        else:
            return package.package_name

    def get_dict_representation(self) -> typing.Dict[str, str]:
        pip_packages = (
            [
                self._get_specification_for_pip_package(pip_package)
                for pip_package in self._pip_installable_packages
            ]
            if self._pip_installable_packages
            else []
        )
        argument_value = ",".join(self._s3_python_wheels + pip_packages)
        return (
            {process_arg_name("additional-python-modules"): argument_value}
            if argument_value
            else {}
        )


class EnableArgument(DefaultArgument):
    arg_name: str

    def __init__(self, enable: bool) -> None:
        self._enable = enable

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return (
            {process_arg_name(self.arg_name): "true"} if self._enable else {}
        )


class EnableAutoscaling(EnableArgument):
    arg_name = "enable-auto-scaling"


class EnableContinuousCloudwatchLog(DefaultArgument):
    def __init__(self, enable: bool, filter_apache_logs: bool):
        self._enable = enable
        self._filter_apache_logs = filter_apache_logs

    def get_dict_representation(self) -> typing.Dict[str, str]:
        if not self._enable:
            return {}
        enable = {process_arg_name("enable-continuous-cloudwatch-log"): "true"}
        filter_name = process_arg_name("enable-continuous-log-filter")
        filter = (
            {filter_name: "true"}
            if self._filter_apache_logs
            else {filter_name: "false"}
        )
        return enable | filter


class EnableGlueCatalog(EnableArgument):
    arg_name = "enable-glue-datacatalog"

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return (
            # We need here to pass an empty string instead of true :wtf:
            # https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-data-catalog-hive.html
            {process_arg_name(self.arg_name): ""}
            if self._enable
            else {}
        )


class EnableMetrics(EnableArgument):
    arg_name = "enable-metrics"


class ExtraFiles(DefaultArgument):
    def __init__(self, s3_file_uris: typing.Sequence["uri.S3Uri"]):
        self._uris = [str(s3_uri) for s3_uri in s3_file_uris]
        for s3_uri in self._uris:
            if s3_uri.endswith("/"):
                raise ValueError("directories are not allowed. uri:", uri)

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {process_arg_name("extra-files"): ",".join(self._uris)}


class ExtraPythonFiles(DefaultArgument):
    def __init__(self, s3_python_file_uris: typing.Sequence["uri.S3Uri"]):
        self._uris = [str(s3_uri) for s3_uri in s3_python_file_uris]
        for s3_uri in self._uris:
            if not s3_uri.endswith(".py"):
                raise ValueError(
                    "Expected python file to end with '.py'", "uri:", s3_uri
                )

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {process_arg_name("extra-py-files"): ",".join(self._uris)}


class JobBookmarkOption(enum.Enum):
    ENABLE = "enable"
    DISABLE = "disable"


class JobBookmark(DefaultArgument):
    def __init__(self, option_value: JobBookmarkOption):
        self._option_value = option_value

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {
            process_arg_name(
                "job-bookmark-option"
            ): f"job-bookmark-{self._option_value.value}"
        }


class TemporaryDirectory(DefaultArgument):
    def __init__(self, s3_path_to_dir: "uri.S3Uri"):
        self._path = s3_path_to_dir

    def get_dict_representation(self) -> typing.Dict[str, str]:
        return {process_arg_name("TempDir"): str(self._path)}
