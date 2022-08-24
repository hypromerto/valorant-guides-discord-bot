from infra.application.app import view_manager


class Guides:

    def __init__(self, command):
        self.command = command

    async def execute(self, message):
        view = view_manager.init_view('GuidesView')

        await message.channel.send("Select an agent and a map:", view=view)
