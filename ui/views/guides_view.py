import discord

from enums.button_action_type import ButtonActionType
from enums.domain_type import DomainType
from infra.config.global_values import s3_client, emoji_data
from ui.message_components.button import Button
from ui.state_machine import calculate_state_transitions_for_guides, calculate_previous_state_transitions_for_guides
from ui.views.pagination_view import PaginationView


class GuidesView(discord.ui.View):

    def __init__(self, component_data, options, base_component_domain_types):
        super().__init__(timeout=None)

        self.component_data = component_data
        self.options = options
        self.content_message = []
        self.current_components = []
        self.current_key_set = []
        self.current_domain_type = None
        self.base_component_domain_types = base_component_domain_types

        for base_type in self.base_component_domain_types:
            for component in self.component_data:
                if base_type == component['domain_type']:

                    # '' is the empty key for base types, as the user
                    # choice does not matter for these selections.
                    for button in self.get_buttons(component['domain_type'], key=''):
                        self.add_item(button)
                        self.current_components.append(button)

                    self.current_domain_type = component['domain_type']

    def get_title(self):
        for component in self.component_data:
            if component['domain_type'] == self.current_domain_type:
                return component['title']

    def add_content_message(self, message):
        self.content_message.append(message)

    def remove_last_content_message(self):
        self.content_message.pop()

    def get_content_message_as_string(self):
        title = ''

        if self.current_domain_type != DomainType.guide_result.name:
            title = self.get_title()

        return '\n'.join(self.content_message) + '\n\n' + title

    def get_buttons(self, domain_type, key):
        buttons = []

        for data_key, data in self.options[domain_type].items():

            if data_key == key:
                for option in data:
                    formatted_label = option.replace(" ", "_")

                    if formatted_label in emoji_data:
                        buttons.append(Button(domain_type=domain_type, emoji=emoji_data[formatted_label],
                                              action=ButtonActionType.guide_button, key=key, value=option, label=option,
                                              style=discord.ButtonStyle.gray))
                    else:
                        buttons.append(
                            Button(domain_type=domain_type, label=option, key=key, action=ButtonActionType.guide_button,
                                   value=option, style=discord.ButtonStyle.gray))

        return buttons

    def go_back_view(self):
        self.current_key_set.pop()
        [self.remove_item(component) for component in self.current_components]
        self.current_components = []

        query_string = '_'.join(self.current_key_set)

        previous_domain_type = calculate_previous_state_transitions_for_guides(self.current_domain_type).name

        for button in self.get_buttons(previous_domain_type, query_string):
            self.add_item(button)
            self.current_components.append(button)

        self.current_domain_type = previous_domain_type

        if previous_domain_type != DomainType.agent.name:
            filter_back_button = Button(ButtonActionType.filter_back.name, emoji='\U000023EA', label='Go Back',
                                        style=discord.ButtonStyle.blurple)
            self.current_components.append(filter_back_button)
            self.add_item(filter_back_button)

        return self

    def update_view(self, value):
        self.current_key_set.append(value)

        [self.remove_item(component) for component in self.current_components]

        self.current_components = []
        query_string = '_'.join(self.current_key_set)

        if self.current_domain_type == DomainType.area.name:

            query = '/'.join(self.current_key_set).lower() + '/'

            options = s3_client.get_all_options(query)

            for option in options:
                side = option.split('-')[0][:-1]

                style = discord.ButtonStyle.green
                if side == 'Attack':
                    style = discord.ButtonStyle.danger

                button = Button(action=ButtonActionType.guide_button, domain_type=DomainType.guide_result.name,
                                label=option, style=style, value=option, key=query_string)
                self.current_components.append(button)
                self.add_item(button)

            self.current_domain_type = DomainType.guide_result.name

        else:
            next_domain_type = calculate_state_transitions_for_guides(self.current_domain_type).name

            for button in self.get_buttons(next_domain_type, query_string):
                self.add_item(button)
                self.current_components.append(button)

            self.current_domain_type = next_domain_type

        filter_back_button = Button(ButtonActionType.filter_back.name, emoji='\U000023EA', label='Go Back',
                                    style=discord.ButtonStyle.blurple)
        self.current_components.append(filter_back_button)
        self.add_item(filter_back_button)

        return self

    def change_to_next_view(self, files, content_message):

        return PaginationView(files, content_message)
