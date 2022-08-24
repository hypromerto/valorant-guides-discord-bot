from client.lineups_client import LineupsClient
from commands.command_manager import CommandManager
from infra.config.config import settings
from ui.views.view_manager import ViewManager

view_manager = ViewManager(settings.views)
# This variable is declared globally, as not all commands utilise views.
# The commands that wish to utilise views can access this variable separately,
# without having to inject the view manager into each command.


def init_bot():
    command_manager = CommandManager(settings.commands)

    client = LineupsClient(prefix=settings.prefix,
                           command_manager=command_manager)

    return client, settings.token
