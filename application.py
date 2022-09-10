import discord
from discord import app_commands

from infra.application.app import init_view
from infra.config.global_values import token
from infra.config.logger import logger


class LineupsClient(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.emojis = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

        print(f'Logged on as {self.user}!')


client = LineupsClient()


@client.tree.command(name="lineups", description="Launch Lineups Guide")
async def lineups(interaction: discord.Interaction):
    logger.info("Lineups command called.")
    view = init_view('guides_view')

    await interaction.response.send_message(content=view.get_content_message_as_string(), view=view)


client.run(token, root_logger=True)
