import discord.ui


class Select(discord.ui.Select):

    def __init__(self, domain_type, options, placeholder, key):
        super().__init__(options=options, placeholder=placeholder)
        self.domain_type = domain_type
        self.key = key

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.edit(view=self.view.update_view(self.domain_type, self.key, self.values[0]))

        await interaction.response.defer()
