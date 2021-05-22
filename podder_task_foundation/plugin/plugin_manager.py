import importlib
from pathlib import Path
from typing import List, Optional, Type

from .._compat import importlib_metadata
from ..objects.object import Object
from ..utilities import Strings


class PluginManager(object):
    def __init__(self, namespace: Optional[str] = None):
        self._ejected_plugin_module_namespace = 'podder_task_foundation_plugins'
        self._namespace = namespace or "podder_task_foundation"
        self._objects = self._load_object_plugins()
        self._commands = self._load_command_plugins()

    def _load_object_plugins(self) -> List[Type]:
        classes = self._load_plugins_from_entry_point("objects")
        classes.extend(self._load_plugins_from_module_directory("objects"))
        return classes

    def _load_command_plugins(self):
        classes = self._load_plugins_from_entry_point("commands")
        classes.extend(self._load_plugins_from_module_directory("commands"))
        return classes

    def _get_entry_point_namespace(self, plugin_type: str) -> str:
        return ".".join([self._namespace, plugin_type])

    def _get_ejected_plugin_module_namespace(self, plugin_type: str) -> str:
        return ".".join([self._ejected_plugin_module_namespace, plugin_type])

    def _load_plugins_from_entry_point(self, plugin_type: str) -> List[Type[Object]]:
        entry_points = importlib_metadata.entry_points().get(
            self._get_entry_point_namespace(plugin_type), ())
        classes = []
        for entry_point in entry_points:
            loader = entry_point.load()
            classes.append(loader())

        return classes

    def _load_plugins_from_module_directory(self, plugin_type: str) -> List[Type[Object]]:
        try:
            objects = importlib.import_module(
                self._get_ejected_plugin_module_namespace(plugin_type))
        except ModuleNotFoundError:
            return []
        directory = Path(objects.__file__).parent
        classes = []
        for plugin in directory.glob("*.py"):
            if plugin.name == "__init__.py":
                continue
            name = plugin.stem
            class_name = Strings().camel_case(name, True)
            try:
                plugin_module = importlib.import_module(
                    'podder_task_foundation_plugins.{}.{}'.format(plugin_type, plugin.stem))
            except ModuleNotFoundError:
                continue
            try:
                _class = getattr(plugin_module, class_name)
            except AttributeError:
                continue
            if issubclass(_class, (Object)):
                classes.append(getattr(plugin_module, class_name))

        return classes

    def get_object_classes(self) -> List[Type[Object]]:
        return self._objects

    def get_command_classes(self):
        return self._commands
