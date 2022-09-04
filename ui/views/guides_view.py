import discord
from discord import SelectOption

from enums.domain_type import DomainType
from infra.config.global_values import s3_client, emoji_data
from ui.message_components.select import Select
from ui.state_machine import calculate_state_transitions_for_guides
from ui.views.pagination_view import PaginationView


class GuidesView(discord.ui.View):

    def __init__(self, component_data, options, base_component_domain_types, state_machine):
        super().__init__(timeout=None)

        self.component_data = component_data
        self.options = options
        self.current_query = []
        self.current_component = ''
        self.base_component_domain_types = base_component_domain_types
        self.state_machine = state_machine

        for base_type in self.base_component_domain_types:
            for component in self.component_data:
                if base_type == component['domain_type']:
                    options_of_select = self.get_options_of_domain_type(component['domain_type'], '')

                    select_object = Select(domain_type=component['domain_type'], placeholder=component['placeholder'],
                                           options=options_of_select, key='')

                    self.add_item(select_object)
                    self.current_component = select_object

                # '' is the empty key for base types, as the user
                # choice does not matter for these selections.

    def get_options_of_domain_type(self, domain_type, key):
        select_options = []

        for data_key, data in self.options[domain_type].items():
            if data_key == key:
                for option in data:
                    formatted_label = option.replace(" ", "_")

                    if formatted_label in emoji_data:
                        select_options.append(SelectOption(label=option, emoji=emoji_data[formatted_label]))
                    else:
                        select_options.append(SelectOption(label=option))

        return select_options

    def update_view(self, current_domain_type, current_key, value):
        query_string = value
        if current_key:
            query_string = '_'.join([current_key, value])

        self.remove_item(self.current_component)

        self.current_component = ''

        if current_domain_type == DomainType.area.name:
            select_options = []

            query = query_string.replace('_', '/').lower() + '/'

            options = s3_client.get_all_options(query)

            for option in options:
                select_options.append(SelectOption(label=option))

            self.add_item(Select(options=select_options, key=query_string, placeholder='Select a lineup...',
                                 domain_type='guide_result'))

        else:
            next_domain_type = calculate_state_transitions_for_guides(current_domain_type).name

            options = self.get_options_of_domain_type(next_domain_type, query_string)

            placeholder = ''
            for component in self.component_data:
                if component['domain_type'] == next_domain_type:
                    placeholder = component['placeholder']
                    break

            select_object = Select(options=options, key=query_string, placeholder=placeholder,
                                   domain_type=next_domain_type)

            self.add_item(select_object)

            self.current_component = select_object

        return self

    def change_to_next_view(self, files, content_message):

        return PaginationView(files, content_message)
