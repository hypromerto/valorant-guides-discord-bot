from infra.application.app import init_view


class Guides:

    def __init__(self, command):
        self.command = command

    async def execute(self, message):
        view = init_view('guides_view')

        await message.channel.send(content=view.get_content_message_as_string(), view=view)
