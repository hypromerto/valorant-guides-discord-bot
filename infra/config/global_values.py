from client.s3_client import S3Client
from infra.config.config import settings

emoji_data = settings.emojis
s3_client = S3Client(settings.aws_access_key_id, settings.aws_secret_access_key)
