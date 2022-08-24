import discord


class GuidesView(discord.ui.View):

    def __init__(self, components):
        super().__init__()
        for component in components:
            self.add_item(component)

