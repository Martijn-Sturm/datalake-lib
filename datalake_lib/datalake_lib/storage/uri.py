class InvalidS3UriException(Exception):
    def __init__(self, value: str, *args: object) -> None:
        message = "S3 uri is invalid"
        super().__init__(message, value, *args)


class S3Uri:
    def __init__(self, value: str) -> None:
        self._value = value
        self._validate_value()

    def __str__(self) -> str:
        return self._value

    def _validate_value(self):
        if " " in self._value:
            raise InvalidS3UriException(
                self._value, "S3 uri contains whitespaces"
            )
        self._validate_head()

    def _validate_head(self):
        expected_head = "s3://"
        if not self._value.startswith("s3://"):
            raise InvalidS3UriException(
                self._value, "S3 uri must start with", expected_head
            )
