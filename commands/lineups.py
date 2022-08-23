import discord


class Lineups():

    def __init__(self, command):
        self.command = command

    async def execute(self, message):
        print('Lineups command is active')