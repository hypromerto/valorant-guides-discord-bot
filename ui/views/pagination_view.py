import discord


class PaginationView(discord.ui.View):

    def __init__(self, components):
        super().__init__()

        self.view_components = components

        for component in components:
            self.add_item(component)
