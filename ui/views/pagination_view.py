import discord

from enums.button_action_type import ButtonActionType


class PaginationView(discord.ui.View):

    def __init__(self, components, files):
        super().__init__()

        self.view_components = components
        self.files = files
        self.current_image_key = 1

        for component in components:

            if component.action == ButtonActionType.back.name or (
                    len(files) == 1 and component.action == ButtonActionType.forward.name):
                component.disabled = True

            self.add_item(component)

    def enable_button_with_type(self, button_type):
        for component in self.view_components:

            if component.action == button_type.name:
                component.disabled = False
