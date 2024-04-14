from io import StringIO
from unittest.mock import MagicMock, create_autospec, patch

import pytest

from app.domain.contracts.logging import Logging
from app.domain.exceptions.file_not_found_exception import \
    FileNotFoundException
from app.domain.exceptions.upload_file_exception import UploadFileException
from app.infra.storage.s3 import S3
from tests.helpers.fake_aws_client import FakeAwsClient
from tests.helpers.generate_entities import make_file

BUCKET_NAME = 'kanastra-imports'
@pytest.fixture
def sut():
    fake_client = FakeAwsClient()
    fake_client.list_buckets = MagicMock(return_value={'Buckets': [BUCKET_NAME]})


    with patch("boto3.client", return_value=fake_client):
        yield S3()




def test_should_create_bucket():

    fake_client = FakeAwsClient()

    fake_client.list_buckets = MagicMock(return_value={'Buckets': []})
    fake_client.create_bucket  = MagicMock()

    with patch("boto3.client", return_value=fake_client):
        S3()

    fake_client.list_buckets.assert_called_once()
    fake_client.create_bucket.assert_called_once_with(Bucket=BUCKET_NAME)


    

def test_get_error_on_upload_file(sut: S3):

    file = make_file()
    sut.s3Client.put_object = MagicMock(side_effect=Exception)

    with pytest.raises(UploadFileException):
        sut.upload(file)

    sut.s3Client.put_object.assert_called_once_with(
        Bucket=BUCKET_NAME,
        Key=f"imports/{file.filename}",
        Body=file.tempFile,
    )

def test_should_upload_with_success(sut: S3):

    file = make_file()
    sut.s3Client.put_object = MagicMock()

    return_file = sut.upload(file)
    assert return_file is not None

    sut.s3Client.put_object.assert_called_once_with(
        Bucket=BUCKET_NAME,
        Key=f"imports/{file.filename}",
        Body=file.tempFile,
    )


def test_get_error_on_load_file(sut: S3):

    file = make_file()
    sut.s3Client.get_object = MagicMock(side_effect=Exception)

    with pytest.raises(FileNotFoundException):
        sut.load(file.filename)

    sut.s3Client.get_object.assert_called_once_with(
        Bucket=BUCKET_NAME,
        Key=f"imports/{file.filename}",
    )

def test_should_read_file_with_success(sut: S3, faker):

    file = make_file()
    file_mock = StringIO(faker.word())
    file_mock.seek(0)

    sut.s3Client.get_object = MagicMock(return_value={'Body': file_mock})

    body = sut.load(file.filename)

    assert body == file_mock.getvalue()

    sut.s3Client.get_object.assert_called_once_with(
        Bucket=BUCKET_NAME,
        Key=f"imports/{file.filename}",
    )