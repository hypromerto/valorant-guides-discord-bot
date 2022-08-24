import discord

from commands.command_manager import CommandManager


class LineupsClient(discord.Client):

    def __init__(self, prefix, command_manager: CommandManager):
        self.prefix = prefix
        self.command_manager = command_manager

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, event):
        if not self.is_valid_message(event):
            return

        # Trimming the prefix
        command = event.content.lstrip(self.prefix)

        await self.command_manager.resolve_and_execute(command, event)

    def is_valid_message(self, message):
        return message.content.startswith(self.prefix) and message.author != self.user
