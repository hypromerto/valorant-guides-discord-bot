import discord


class SelectOption(discord.SelectOption):

    def __init__(self, label, key):
        super().__init__(label=label)
        self.key = key
