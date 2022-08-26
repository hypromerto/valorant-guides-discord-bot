import discord.ui


class Select(discord.ui.Select):

    def __init__(self, domain_type, options, placeholder):
        super().__init__(options=options, placeholder=placeholder)
        self.domain_type = domain_type

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Your choice is {self.values[0]}!", ephemeral=False)

        self.view.update_view(self.values[0])
