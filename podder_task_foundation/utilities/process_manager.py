from pathlib import Path
from typing import Dict, Optional

from ..config import ProcessConfig, SharedConfig


class ProcessManager(object):
    def __init__(self, mode: str, shared_config: SharedConfig = None, debug_mode: bool = False):
        self._mode = mode
        self._shared_config = shared_config
        self._debug_mode = debug_mode
        self._root_path = Path(self._shared_config.get('file.root_directory', './')).absolute()

    def get_process_list(self) -> Dict[str, Optional[Dict]]:
        processes_path = self._root_path.joinpath("processes")
        processes = {}
        for path in processes_path.iterdir():
            if path.is_dir() and not path.name.startswith("_"):
                processes[path.name] = self.get_process_interface(path.name)

        return processes

    def get_process_interface(self, process_name: str):
        config = self.get_process_config(process_name)
        if config is None:
            return None

        return config.get("interface")

    def get_process_config(self, process_name: str) -> ProcessConfig:
        return ProcessConfig(self._mode, process_name=process_name, path=self._shared_config.path)
