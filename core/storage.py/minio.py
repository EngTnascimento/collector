from minio import Minio
from minio.error import S3Error

from core.config import settings


class MinioStorage:
    def __init__(self) -> None:
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_key,
            secret_key=settings.minio_secret,
            secure=False,
        )

    def create_bucket(self, bucket_name: str):
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' created successfully.")
            else:
                print(f"Bucket '{bucket_name}' already exists.")
        except S3Error as err:
            print(f"Error creating bucket '{bucket_name}': {err}")

    def upload(self, bucket_name, object_name, data):
        try:
            self.client.put_object(bucket_name, object_name, data, len(data))
            print(f"Data '{object_name}' uploaded successfully.")
        except S3Error as err:
            print(f"Error uploading data: {err}")
