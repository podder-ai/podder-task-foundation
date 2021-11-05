from argparse import Namespace

from ..parameters import Parameters


class Command(object):
    name = ""
    aliases = []
    help = ""
    type = "command"

    def add_command(self, sub_commands):
        parser = self._set_sub_command(sub_commands)
        self.set_arguments(parser)
        self._set_handler(parser)
        return parser

    def _set_sub_command(self, sub_commands):
        parser = sub_commands.add_parser(self.name, aliases=self.aliases, help=self.help)
        return parser

    def _set_handler(self, parser):
        parser.set_defaults(func=self.handler)

    def set_arguments(self, parser):
        pass

    def handler(self, arguments: Namespace, unknown_arguments: Parameters, *args):
        pass
