# AWS S3 configuration
AWS_ACCESS_KEY_ID = "development"  # Use any test credentials
AWS_SECRET_ACCESS_KEY = "development"  # Use any test credentials
AWS_STORAGE_BUCKET_NAME = "selected-element-html-s3-bucket"
AWS_S3_ENDPOINT_URL = "http://localhost:4566"
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_CUSTOM_DOMAIN = f"localhost:4566/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Add this setting to handle file URLs
AWS_S3_ADDRESSING_STYLE = "path"
