
from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config

class StaticStorage(S3Boto3Storage):
    location = 'militerystatic'
    bucket_name = config('AWS_STORAGE_BUCKET_NAME')


class PublicMediaStorage(S3Boto3Storage):
    location = 'militerymedia'
    file_overwrite = False
    bucket_name = config('AWS_STORAGE_BUCKET_NAME')