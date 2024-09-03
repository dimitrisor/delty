from app import env

# AWS S3 configuration
AWS_ACCESS_KEY_ID = env.get_str("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = env.get_str("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = env.get_str("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_ENDPOINT_URL = env.get_str("AWS_S3_ENDPOINT_URL", "")
AWS_S3_REGION_NAME = env.get_str("AWS_S3_REGION_NAME", "")
# AWS_S3_CUSTOM_DOMAIN = env.get_str(
#     "AWS_S3_CUSTOM_DOMAIN", ""
# )
# AWS_S3_FILE_OVERWRITE = env.get_bool("AWS_S3_FILE_OVERWRITE", False)
# AWS_DEFAULT_ACL = None
AWS_S3_SECURE_URLS = env.get_bool("AWS_S3_SECURE_URLS", False)
AWS_S3_USE_SSL = env.get_bool("AWS_S3_USE_SSL", False)
