import discord

from commands.command_manager import CommandManager

class LineupsClient(discord.Client):

    def __init__(self, prefix, command_manager: CommandManager):
        self.prefix = prefix
        self.command_manager = command_manager
        super().__init__()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        await self.command_manager.resolve(message.content).execute(message)