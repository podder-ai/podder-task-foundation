from pathlib import Path
from typing import Optional

from .config import Config
from .context import Context
from .mode import MODE


class CommandExecutor(object):
    def __init__(self,
                 config_path: Optional[str],
                 mode: str = MODE.CONSOLE,
                 verbose: bool = False,
                 debug_mode: bool = False):
        if config_path is None or config_path == "":
            config_path_object = Path(Config.default_path)
        else:
            config_path_object = Path(config_path)

        self._context = Context(mode=mode,
                                config_path=config_path_object,
                                debug_mode=debug_mode,
                                verbose=verbose)

    @property
    def context(self) -> Context:
        return self._context

    def execute(self, command_name: str):

        if self._context.debug_mode:
            self._context.logger.debug("Debug mode enabled")
        self._execute_command(command_name, self._context)

    @staticmethod
    def _execute_command(name: str, context: Context):
        from .plugin import Command, PluginManager
        _commands: [Command] = PluginManager().get_command_classes()
        for command in _commands:
            if command.name == name:
                command().execute(context)
                return

        raise Exception("Command {} does not exist.".format(name))
