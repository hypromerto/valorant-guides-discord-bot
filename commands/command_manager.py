import importlib


def inject_commands(command_strings):
    command_map = {}

    for command in command_strings:
        module = importlib.import_module('.' + command,
                                         package=__package__)

        CommandClass = getattr(module, command.capitalize())

        instance = CommandClass(command)

        command_map[command] = instance

    return command_map


class CommandManager:

    '''
    Command map structure:
    {
        'guides': Guides Command Object,
        'help': Help Command Object
    }
    '''

    def __init__(self, command_strings):
        self.command_map = inject_commands(command_strings)

    async def resolve_and_execute(self, command, event):
        if command in self.command_map:
            await self.command_map[command].execute(event)
        else:
            await event.channel.send("Invalid command.")
