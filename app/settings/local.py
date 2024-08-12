from app import env
from app.settings.base import *  # noqa

DEBUG = env.get_bool("DEBUG", default=True)
ENVIRONMENT = "local"

# AWS S3 configuration
AWS_ACCESS_KEY_ID = env.get_str("AWS_ACCESS_KEY_ID", "development")
AWS_SECRET_ACCESS_KEY = env.get_str("AWS_SECRET_ACCESS_KEY", "development")
AWS_STORAGE_BUCKET_NAME = env.get_str(
    "AWS_STORAGE_BUCKET_NAME", "selected-element-html-s3-bucket"
)
AWS_S3_ENDPOINT_URL = env.get_str("AWS_S3_HOST", "http://localhost:4566")
AWS_S3_REGION_NAME = env.get_str("AWS_S3_REGION_NAME", "us-east-1")
