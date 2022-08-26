import discord.ui

class Select(discord.ui.Select):

    def __init__(self, domain_type, options, placeholder):
        super().__init__(options=options, placeholder=placeholder)
        self.domain_type = domain_type

