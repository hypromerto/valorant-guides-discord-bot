import io

import discord.ui

from enums.button_action_type import ButtonActionType
from enums.domain_type import DomainType
from infra.config.global_values import emoji_data, s3_client
from infra.config.logger import logger


class Button(discord.ui.Button):

    def __init__(self, action, value=None, emoji=None, domain_type=None, key=None, label=None, style=None):
        super().__init__(emoji=emoji, label=label, style=style)
        self.action = action
        self.domain_type = domain_type
        self.value = value
        self.key = key

    async def callback(self, interaction: discord.Interaction):

        if self.action == ButtonActionType.photo_back.name or self.action == ButtonActionType.photo_forward.name:
            await self.execute_ui_button_callback(interaction)
        elif self.action == ButtonActionType.filter_back.name:
            await self.execute_filter_back_button_callback(interaction)
        else:
            await self.execute_guide_button_callback(interaction)

    async def execute_filter_back_button_callback(self, interaction: discord.Interaction):
        updated_view = self.view.go_back_view()

        self.view.remove_last_content_message()

        await interaction.message.edit(content=self.view.get_content_message_as_string(),
                                       view=updated_view)

        await interaction.response.defer()


    async def execute_guide_button_callback(self, interaction: discord.Interaction):
        content_message = self.prepare_message()

        if self.domain_type != DomainType.guide_result.name:
            updated_view = self.view.update_view(self.value)
            self.view.add_content_message(content_message)

            await interaction.message.edit(content=self.view.get_content_message_as_string(),
                                           view=updated_view)

            await interaction.response.defer()
        else:
            await interaction.response.defer(thinking=True)
            query_dir = self.key.replace('_', '/').lower() + '/' + self.value + '/'

            files = s3_client.download_all_objects(query_dir)

            if files:
                logger.info(f'Successfully downloaded {len(files)} files.')

                next_view = self.view.change_to_next_view(files, content_message)

                file = discord.File(io.BytesIO(files[1]), filename='image.png')

                await interaction.followup.send(file=file, content=content_message, view=next_view)

    async def execute_ui_button_callback(self, interaction: discord.Interaction):

        next_image = ''

        next_image_index = self.view.current_image_key

        if self.action == ButtonActionType.photo_back.name:

            next_image_index = self.view.current_image_key - 1

            if next_image_index == 1:
                self.disabled = True

            self.view.enable_button_with_type(ButtonActionType.photo_forward)

            next_image = self.view.files[next_image_index]
        elif self.action == ButtonActionType.photo_forward.name:

            next_image_index = self.view.current_image_key + 1
            image_count = len(self.view.files)

            if next_image_index == image_count:
                self.disabled = True

            self.view.enable_button_with_type(ButtonActionType.photo_back)

            next_image = self.view.files[next_image_index]

        self.view.current_image_key = next_image_index

        next_image = discord.File(io.BytesIO(next_image), filename=f'{next_image_index}.png')

        await interaction.response.edit_message(content=self.view.content_message, attachments=[next_image],
                                                view=self.view)

    def prepare_message(self):
        if self.domain_type == DomainType.guide_result.name:
            return f'**{self.value}**'

        emoji_value = ""
        formatted_emoji_key = self.value.replace(' ', '_')
        if formatted_emoji_key in emoji_data:
            emoji_value = emoji_data[formatted_emoji_key]

        content_message = f'**{self.domain_type.capitalize()}:**  {emoji_value} {self.value}'

        return content_message
