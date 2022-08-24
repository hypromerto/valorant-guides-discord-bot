import discord.ui

from enums.select_type import SelectType


class Select(discord.ui.Select):

    def __init__(self, select_type: SelectType, options, placeholder):
        super().__init__()
        self.select_type = select_type
        self.options = options
        self.placeholder = placeholder


