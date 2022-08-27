import discord
from discord import SelectOption

from enums.domain_type import DomainType
from infra.config.global_values import s3_client
from ui.message_components.select import Select
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

        self.remove_item(self.view_components[current_domain_type][current_key])

        if current_domain_type == DomainType.area.name:
            select_options = []

            query = query_string.replace('_', '/').lower() + '/'

            options = s3_client.get_all_options(query)

            for option in options:
                select_options.append(SelectOption(label=option))

            self.add_item(Select(options=select_options, key=query_string, placeholder='Select a lineup...',
                                 domain_type='guide_result'))

        else:
            next_domain_type = calculate_state_transitions_for_guides(current_domain_type)

            self.add_item(self.view_components[next_domain_type.name][query_string])

        return self

    def change_to_next_view(self, files):
        return PaginationView(self.state_machine.get_next_view('guides_view')['components'], files)
