import discord.ui


class Button(discord.ui.Button):

    def __init__(self, emoji):
        super().__init__(emoji=emoji)

    async def callback(self, interaction: discord.Interaction):
        print("dasdfa")
