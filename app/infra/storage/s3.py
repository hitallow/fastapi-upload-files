import os

import boto3

from app.domain.contracts.storage import Storage
from app.domain.entities.file import File
from app.domain.exceptions.file_not_found_exception import \
    FileNotFoundException
from app.domain.exceptions.upload_file_exception import UploadFileException


class S3(Storage):
    __bucket_name = "kanastra-imports"

    def __init__(self) -> None:
        self.s3Client = boto3.client(
            service_name="s3",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=os.getenv('AWS_URL'),
        )

        self._create_bucket()

    def _create_bucket(self):
        if self.__bucket_name not in self.s3Client.list_buckets()["Buckets"]:
            self.s3Client.create_bucket(Bucket=self.__bucket_name)

    def upload(self, file: File) -> File:
        try:
            self.s3Client.put_object(
                Bucket=self.__bucket_name,
                Key=f"imports/{file.filename}",
                Body=file.tempFile,
            )
            return file
        except Exception as error:
            raise UploadFileException() from error

    def load(self, filename: str) -> bytes:
        try:
            res = self.s3Client.get_object(
                Bucket=self.__bucket_name,
                Key=f"imports/{filename}",
            )
            return res["Body"].read()
        except Exception as error:
            raise FileNotFoundException() from error
