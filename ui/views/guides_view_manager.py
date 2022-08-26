import discord

from enums.domain_type import DomainType
from enums.view_type import ViewType
from ui.message_components.select import Select
from ui.views.guides_view import GuidesView


def get_options(domain_type, agent_guides_data):
    options = []

    if domain_type == DomainType.AGENT.name:
        for agent_data in agent_guides_data:
            options.append(agent_data['agent'])

    return options


def init_components_of_view(components, agent_guides_data):
    view_components = []

    for component in components:
        if component["type"] == discord.ComponentType.select.name:
            select_options = []

            for option in get_options(component['domain_type'], agent_guides_data):
                select_options.append(discord.SelectOption(label=option))

            view_components.append(Select(domain_type=component['domain_type'], placeholder=component['placeholder'],
                                          options=select_options))

    return view_components


def inject_views(views, agent_guides_data):
    view_map = {}

    for view in views:
        class_name = ''.join(map(lambda name: name.capitalize(), view["name"].split('_')))

        components = init_components_of_view(view['components'], agent_guides_data)

        view_map[class_name] = {'components': components, 'base_component_domain_types': view['base_component_domain_types']}

    return view_map


class GuidesViewManager:
    """Manages all the views of the commands.

        This class injects all the properties of a view, but it does not instantiate them.
        This is because view instantiation must be done during runtime, in an event loop.
    """

    def __init__(self, views, agent_guides_data):
        self.view_map = inject_views(views, agent_guides_data)

    def init_view(self, view_class_name):
        if view_class_name in self.view_map:

            if view_class_name == ViewType.GuidesView.name:
                return GuidesView(self.view_map[view_class_name]['components'], self.view_map[view_class_name]['base_component_domain_types'])
