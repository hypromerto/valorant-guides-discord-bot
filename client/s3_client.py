import io

import boto3


class S3Client:

    def __init__(self, access_key_id, secret_access_key):
        self.bucket_name = 'valorant-guide-bot'
        self.s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    def get_all_options(self, query):
        options = []

        folder_result = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=query, Delimiter='/')

        for prefix in folder_result['CommonPrefixes']:
            options.append(prefix['Prefix'][:-1].rsplit('/', 1)[-1])

        return options

    def download_all_objects(self, query_dir):
        files = {}

        buf = io.BytesIO()

        obj_results = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=query_dir, Delimiter='/')

        for obj in obj_results['Contents']:

            if obj['Key'] == query_dir:
                continue

            file_name = int((obj['Key'].rsplit('/', 1)[-1]).split('.', 1)[0])

            self.s3_client.download_fileobj(self.bucket_name, obj['Key'], buf)
            file_content = buf.getvalue()

            files[file_name] = file_content

        return files
