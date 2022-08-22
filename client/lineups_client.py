import discord

class LineupsClient(discord.Client):

    def __init__(self, prefix):
        self.prefix = prefix
        super().__init__()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')