from client.lineups_client import LineupsClient
from commands.command_manager import CommandManager
from enums.view_type import ViewType
from infra.config.config import settings
from infra.config.global_values import emoji_data
from ui.state_machine import StateMachine
from ui.views.guides_view import GuidesView
from ui.views.pagination_view import PaginationView
from ui.views.view_manager import inject_views

view_map = inject_views(settings.views, settings.agent_guides_data)

# This variable is declared globally, as not all commands utilise views.
# The commands that wish to utilise views can access this variable separately,
# without having to inject the view manager into each command.

state_machine = StateMachine(view_map)


def init_bot():
    command_manager = CommandManager(settings.commands)

    client = LineupsClient(prefix=settings.prefix,
                           command_manager=command_manager)

    return client, settings.token


def init_view(view_type):
    if view_type in view_map:

        if view_type == ViewType.guides_view.name:
            for key, val in view_map[view_type]['components'].items():
                for key, val in val.items():
                    for option in val.options:

                        formatted_option = option.label.replace(" ", "_")

                        if formatted_option in emoji_data:
                            option.emoji = emoji_data[formatted_option]

            return GuidesView(view_map[view_type]['components'],
                              view_map[view_type]['base_component_domain_types'], state_machine)

        elif view_type == ViewType.pagination_view.name:

            return PaginationView(view_map[view_type]['components'])
