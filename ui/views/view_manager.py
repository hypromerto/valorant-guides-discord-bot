import discord

from enums.view_type import ViewType
from ui.message_components.select import Select
from ui.views.guides_view import GuidesView


def init_components_of_view(components):
    view_components = []

    for component in components:
        if component["type"] == discord.ComponentType.select.name:
            select_options = []

            for option in component['options']:
                select_options.append(discord.SelectOption(label=option))

            view_components.append(Select(component['domain_type'], select_options))

    return view_components


def inject_views(views):
    view_map = {}

    for view in views:
        class_name = ''.join(map(lambda name: name.capitalize(), view["name"].split('_')))

        components = init_components_of_view(view['components'])

        view_map[class_name] = {'components': components}

    return view_map


class ViewManager:

    """Manages all the views of the commands.

        This class injects all the properties of a view, but it does not instantiate them.
        This is because view instantiation must be done during runtime, in an event loop.
    """

    def __init__(self, views):
        self.view_map = inject_views(views)

    def init_view(self, view_class_name):
        if view_class_name in self.view_map:

            if view_class_name == ViewType.GuidesView.name:
                return GuidesView(self.view_map[view_class_name]['components'])
