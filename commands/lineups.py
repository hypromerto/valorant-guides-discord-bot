import discord


class Lineups():

    def __init__(self, command):
        self.command = command

    async def execute(self, message):
        await message.channel.send("Lineups")   