import discord

from ui.state_machine import calculate_state_transitions_for_guides
from ui.views.pagination_view import PaginationView


class GuidesView(discord.ui.View):

    def __init__(self, components, base_component_domain_types, state_machine):
        super().__init__()

        self.view_components = components
        self.current_query = []
        self.base_component_domain_types = base_component_domain_types
        self.state_machine = state_machine

        for base_type in self.base_component_domain_types:
            if base_type in self.view_components:
                self.add_item(self.view_components[base_type][''])
                # '' is the empty key for base types, as the user
                # choice does not matter for these selections.

    def update_view(self, current_domain_type, current_key, value):
        query_string = value
        if current_key:
            query_string = '_'.join([current_key, value])

        next_domain_type = calculate_state_transitions_for_guides(current_domain_type)
        self.remove_item(self.view_components[current_domain_type][current_key])

        self.add_item(self.view_components[next_domain_type.name][query_string])

        return self

    def change_to_next_view(self):
        return PaginationView(self.state_machine.get_next_view('guides_view')['components'])
