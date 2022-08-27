import discord


class PaginationView(discord.ui.View):

    def __init__(self, components, files):
        super().__init__()

        self.view_components = components
        self.files = files

        for component in components:
            self.add_item(component)
