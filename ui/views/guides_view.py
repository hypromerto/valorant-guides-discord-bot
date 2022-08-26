import discord

from ui.state_machine import calculate_state_transitions_for_guides


class GuidesView(discord.ui.View):

    def __init__(self, components, base_component_domain_types):
        super().__init__()

        self.view_components = components
        self.current_query = []
        self.base_component_domain_types = base_component_domain_types

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
