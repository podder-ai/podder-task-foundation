from ..plugin import CommandPluginManager
from .execute import Execute

_commands = CommandPluginManager().get_classes()
_commands.extend([Execute])


def load_commands(sub_commands) -> [str]:
    command_names = []
    for _command in _commands:
        _command().add_command(sub_commands)
        command_names.append(_command.name)
        command_names.extend(_command.aliases)

    return command_names


__all__ = ["Execute", "load_commands"]
