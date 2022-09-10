import discord

from enums.button_action_type import ButtonActionType
from enums.domain_type import DomainType
from ui.message_components.button import Button


def init_pagination_view_components():
    back_button = Button(emoji='\U000023EA', action=ButtonActionType.back.name, style=discord.ButtonStyle.gray, domain_type=DomainType.ui_button.name)
    forward_button = Button(emoji='\U000023E9', action=ButtonActionType.forward.name, style=discord.ButtonStyle.gray, domain_type=DomainType.ui_button.name)

    return [back_button, forward_button]


class PaginationView(discord.ui.View):

    def __init__(self, files, content_message):
        super().__init__(timeout=None)

        self.view_components = init_pagination_view_components()
        self.files = files
        self.current_image_key = 1
        self.content_message = content_message

        for component in self.view_components:

            if component.action == ButtonActionType.back.name or (
                    len(files) == 1 and component.action == ButtonActionType.forward.name):
                component.disabled = True

            self.add_item(component)

    def enable_button_with_type(self, button_type):
        for component in self.view_components:

            if component.action == button_type.name:
                component.disabled = False
