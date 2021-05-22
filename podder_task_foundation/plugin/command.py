from ..context import Context


class Command(object):
    name = "command_name"

    def execute(self, context: Context):
        raise NotImplementedError
