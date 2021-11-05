import argparse
import sys

from .commands import load_commands
from .parameters import Parameters


class CLI(object):
    def __init__(self):
        self._command_names = []
        self._parser = self._get_parser()

    def _get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Podder Task CLI Argument Parser')
        subparsers = parser.add_subparsers()
        self._command_names = load_commands(subparsers)
        return parser

    def execute(self):
        command_arguments = sys.argv[1:]
        if len(command_arguments) > 0:
            command_name = command_arguments[0]
            if command_name not in self._command_names:
                new_command_arguments = ["execute"]
                new_command_arguments.extend(command_arguments)
                command_arguments = new_command_arguments

        arguments, unknown_arguments = self._parser.parse_known_args(command_arguments)
        if hasattr(arguments, 'func'):
            arguments.func(arguments, Parameters.from_cli_params(unknown_arguments))
        else:
            self._parser.print_help()
