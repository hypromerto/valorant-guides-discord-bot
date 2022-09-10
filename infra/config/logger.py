import logging
import time

import boto3
import watchtower


class NoSetupLogsFilter(logging.Filter):
    def filter(self, record):
        filter_words = ["Shard"]

        for word in filter_words:
            if word in record.getMessage():
                return False

        return True


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("root")

dt_fmt = '%d-%m-%Y %H:%M:%S'
logs_client = boto3.client("logs", region_name="eu-central-1")

handler = watchtower.CloudWatchLogHandler(log_group_name="valorant-guides-bot", log_stream_name="ec2-stream", boto3_client=logs_client)

formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

handler.setFormatter(formatter)
handler.addFilter(NoSetupLogsFilter())

logger.addHandler(handler)
