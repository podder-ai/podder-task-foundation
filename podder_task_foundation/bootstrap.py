import importlib

from .context import Context


def bootstrap(context: Context) -> bool:
    return Bootstrap(context).execute()


class Bootstrap(object):

    def __init__(self, context: Context):
        self._context = context

    def execute(self) -> bool:
        return self._execute_process_bootstraps()

    def _execute_process_bootstraps(self) -> bool:
        processes = self._context.process_manager.get_process_list()
        for name, process in processes.items():
            process_object = importlib.import_module('processes.{}.process'.format(name))
            process_object.bootstrap(self._context.mode, process)

        return True
