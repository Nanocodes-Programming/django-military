
from storages.backends.s3boto3 import S3Boto3Storage
import os

class StaticStorage(S3Boto3Storage):
    location = 'militerystatic'
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')


class PublicMediaStorage(S3Boto3Storage):
    location = 'militerymedia'
    file_overwrite = False
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')