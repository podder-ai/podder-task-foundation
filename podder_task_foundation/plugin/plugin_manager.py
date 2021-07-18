import importlib
import importlib.machinery
import os
from pathlib import Path
from typing import Any, List, Optional, Type

from .._compat import importlib_metadata
from ..utilities import Strings


class PluginManager(object):
    namespace = ""

    def __init__(self, namespace: Optional[str] = None):
        self._ejected_plugin_module_namespace = 'podder_task_foundation_plugins'
        self._namespace = namespace or "podder_task_foundation"
        self._plugins = self._load_plugins()

    def _load_plugins(self) -> List[Any]:
        classes = self._load_plugins_from_entry_point(self.namespace)
        classes.extend(self._load_plugins_from_module_directory(self.namespace))
        return classes

    def get_classes(self) -> List[Any]:
        return self._plugins

    def _get_entry_point_namespace(self, plugin_type: str) -> str:
        return ".".join([self._namespace, plugin_type])

    def _get_ejected_plugin_module_namespace(self, plugin_type: str) -> str:
        return ".".join([self._ejected_plugin_module_namespace, plugin_type])

    def _load_plugins_from_entry_point(self, plugin_type: str) -> List[Type[Any]]:
        entry_points = importlib_metadata.entry_points().get(
            self._get_entry_point_namespace(plugin_type), ())
        classes = []
        for entry_point in entry_points:
            loader = entry_point.load()
            classes.append(loader())

        return classes

    def _load_plugins_from_module_directory(self, plugin_type: str) -> List[Type]:
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
            if hasattr(_class, "type") and _class.type == "plugin_type":
                classes.append(getattr(plugin_module, class_name))

        directory_plugins = set([str(x.parent) for x in list(directory.glob("*/*.py"))])
        for plugin_directory in directory_plugins:
            plugin_module_name = ".".join(plugin_directory.split(os.sep))
            plugin_module_object = importlib.machinery.SourceFileLoader(
                plugin_module_name, str(Path(plugin_directory).joinpath("__init__.py")))
            plugin_module = plugin_module_object.load_module()
            classes.append(plugin_module.get_class())

        return classes
