from client.lineups_client import LineupsClient
from commands.command_manager import CommandManager
from infra.config.config import settings
from ui.views.guides_view_manager import GuidesViewManager

view_manager = GuidesViewManager(settings.views, settings.agent_guides_data)
# This variable is declared globally, as not all commands utilise views.
# The commands that wish to utilise views can access this variable separately,
# without having to inject the view manager into each command.


def init_bot():
    command_manager = CommandManager(settings.commands)

    client = LineupsClient(prefix=settings.prefix,
                           command_manager=command_manager)

    return client, settings.token
