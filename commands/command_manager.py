import importlib


class CommandManager():

    def __init__(self, command_strings):
        self.command_map = self.inject_commands(command_strings)

    def inject_commands(self, command_strings):
        command_map = {}

        for command in command_strings:
            module = importlib.import_module('.' + command,
                                             package=__package__)

            CommandClass = getattr(module, command.capitalize())

            instance = CommandClass(command)

            command_map[command] = instance

        return command_map

    async def resolve_and_execute(self, command, event):
        if command in self.command_map:
            await self.command_map[command].execute(event)
        else:
            await event.channel.send("Invalid command.")
