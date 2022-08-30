from client.s3_client import S3Client
from infra.config.config import settings

from infra.config.secret_manager import get_secret

secrets = get_secret()
token = secrets['token']


emoji_data = settings.emojis
s3_client = S3Client()
