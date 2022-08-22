from client.lineups_client import LineupsClient
from infra.config.config import settings


def init_bot():

    client = LineupsClient(prefix=settings.prefix)

    return client, settings.token