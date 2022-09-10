import discord
from discord import app_commands

from infra.application.app import init_view
from infra.config.global_values import token


class LineupsClient(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.emojis = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()

        print(f'Logged on as {self.user}!')


client = LineupsClient()


@client.tree.command(name="lineups", description="Launch Lineups Guide", guild=discord.Object(id=1008859001380937788))
async def test(interaction: discord.Interaction):
    view = init_view('guides_view')

    await interaction.response.send_message(content=view.get_content_message_as_string(), view=view)


client.run(token)
