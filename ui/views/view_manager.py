import discord

from enums.domain_type import DomainType
from enums.view_type import ViewType
from ui.message_components.select import Select
from ui.state_machine import StateMachine
from ui.views.guides_view import GuidesView


def get_guide_options(domain_type, agent_guides_data):
    options = []

    if domain_type == DomainType.AGENT.name:
        for agent_data in agent_guides_data:
            options.append(agent_data['agent'])

    return options


def init_guides_view_components(components, agent_guides_data):
    view_components = []

    for component in components:
        if component["type"] == discord.ComponentType.select.name:
            select_options = []

            for option in get_guide_options(component['domain_type'], agent_guides_data):
                select_options.append(discord.SelectOption(label=option))

            view_components.append(Select(domain_type=component['domain_type'], placeholder=component['placeholder'],
                                          options=select_options))

    return view_components


def inject_views(views, agent_guides_data):
    view_map = {}

    for view in views:
        components = []
        if view['view_type'] == ViewType.GUIDES_VIEW.name:
            components = init_guides_view_components(view['components'], agent_guides_data)

        view_map[view["view_type"]] = {'components': components,
                                       'base_component_domain_types': view['base_component_domain_types']}

    return view_map


class ViewManager:
    """Manages all the views of the commands.

        This class injects all the properties of a view, but it does not instantiate them.
        This is because view instantiation must be done during runtime, in an event loop.
    """

    def __init__(self, views, agent_guides_data):
        self.view_map = inject_views(views, agent_guides_data)

    def init_view(self, view_type):
        if view_type in self.view_map:

            if view_type == ViewType.GUIDES_VIEW.name:
                return GuidesView(self.view_map[view_type]['components'],
                                  self.view_map[view_type]['base_component_domain_types'], StateMachine())
