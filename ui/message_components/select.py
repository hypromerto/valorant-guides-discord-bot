import io

import discord.ui

from enums.domain_type import DomainType
from infra.config.global_values import emoji_data, s3_client


class Select(discord.ui.Select):

    def __init__(self, domain_type, options, placeholder, key):
        super().__init__(options=options, placeholder=placeholder)
        self.domain_type = domain_type
        self.key = key

    async def callback(self, interaction: discord.Interaction):
        content_message = self.prepare_message()

        if self.domain_type != DomainType.guide_result.name:

            updated_view = self.view.update_view(self.values[0])

            await interaction.message.edit(content=content_message,
                                           view=updated_view)

            await interaction.response.defer()
        else:

            query_dir = self.key.replace('_', '/').lower() + '/' + self.values[0] + '/'

            files = s3_client.download_all_objects(query_dir)

            if files:
                next_view = self.view.change_to_next_view(files, content_message)

                file = discord.File(io.BytesIO(files[1]), filename='image.png')

                await interaction.response.send_message(file=file, content=content_message, view=next_view)

    def prepare_message(self):

        if self.domain_type == DomainType.guide_result.name:
            return f'**{self.values[0]}**'

        emoji_value = ""
        formatted_emoji_key = self.values[0].replace(' ', '_')
        if formatted_emoji_key in emoji_data:
            emoji_value = emoji_data[formatted_emoji_key]

        content_message = f'**{self.domain_type.capitalize()}:**  {emoji_value} {self.values[0]}'

        return content_message
