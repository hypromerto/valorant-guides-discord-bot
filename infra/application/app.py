from client.lineups_client import LineupsClient
from commands.command_manager import CommandManager
from infra.config.config import settings


def init_bot():

    command_manager = CommandManager(settings.commands)

    client = LineupsClient(prefix=settings.prefix,
                           command_manager=command_manager)

    return client, settings.token
