import io

import discord.ui

from enums.button_action_type import ButtonActionType


class Button(discord.ui.Button):

    def __init__(self, emoji, action):
        super().__init__(emoji=emoji)
        self.action = action

    async def callback(self, interaction: discord.Interaction):

        next_image = ''

        next_image_index = self.view.current_image_key

        if self.action == ButtonActionType.back.name:

            next_image_index = self.view.current_image_key - 1

            if next_image_index == 1:
                self.disabled = True

            self.view.enable_button_with_type(ButtonActionType.forward)

            next_image = self.view.files[next_image_index]
        elif self.action == ButtonActionType.forward.name:

            next_image_index = self.view.current_image_key + 1
            image_count = len(self.view.files)

            if next_image_index == image_count:
                self.disabled = True

            self.view.enable_button_with_type(ButtonActionType.back)

            next_image = self.view.files[next_image_index]

        self.view.current_image_key = next_image_index

        next_image = discord.File(io.BytesIO(next_image), filename=f'{next_image_index}.png')

        await interaction.response.send_message(content=self.view.content_message, file=next_image, view=self.view)

        await interaction.message.delete()
