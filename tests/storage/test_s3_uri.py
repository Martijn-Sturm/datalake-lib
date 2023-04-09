from datalake_lib.storage import uri
import pytest


def test_s3_uri_raises_if_invalid_uri_start():
    with pytest.raises(uri.InvalidS3UriException):
        uri.S3Uri("file://does/not/start/with/s3/anchor/but/doesnt")


def test_s3_uri_raises_if_not_pathlike():
    with pytest.raises(uri.InvalidS3UriException):
        uri.S3Uri("s3:// not a pathlike value")
