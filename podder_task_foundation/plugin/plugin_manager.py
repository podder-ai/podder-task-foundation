import importlib
from pathlib import Path
from typing import List, Optional, Type

from .._compat import importlib_metadata
from ..objects.object import Object


class PluginManager(object):
    _local_plugin_module_namespace = 'podder_task_foundation_plugins.objects'

    def __init__(self, namespace: Optional[str] = None):
        self._namespace = namespace or "podder_task_foundation.objects"
        self._filetypes = self._load_filetype_plugins()

    def _load_filetype_plugins(self) -> List[Type[Object]]:
        classes = self._load_filetype_plugins_from_entry_point()
        classes.extend(self._load_filetype_plugins_from_module_directory())
        return classes

    def _load_filetype_plugins_from_entry_point(self) -> List[Type[Object]]:
        entry_points = importlib_metadata.entry_points().get(self._namespace, ())
        classes = []
        for entry_point in entry_points:
            loader = entry_point.load()
            classes.append(loader())

        return classes

    def _load_filetype_plugins_from_module_directory(self) -> List[Type[Object]]:
        try:
            objects = importlib.import_module(self._local_plugin_module_namespace)
        except ModuleNotFoundError:
            return []
        directory = Path(objects.__file__).parent
        classes = []
        for plugin in directory.glob("*.py"):
            name = plugin.stem
            plugin_module = importlib.import_module(
                'podder_task_foundation_plugins.objects.{}'.format(plugin.stem))
            classes.append(getattr(plugin_module, name))

        return classes

    def get_filetype_classes(self) -> List[Type[Object]]:
        return self._filetypes
