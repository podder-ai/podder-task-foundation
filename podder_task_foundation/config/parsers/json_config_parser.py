import json
from collections import OrderedDict
from pathlib import Path

from podder_task_foundation.config.parsers.base_config_parser import \
    BaseConfigParser


class JsonConfigParser(BaseConfigParser):
    @classmethod
    def name(cls) -> str:
        return "json"

    @classmethod
    def detect_target(cls, file: Path) -> bool:
        if file.suffix.lower() == '.json':
            return True

        return False

    @classmethod
    def parse(cls, file) -> dict:
        return json.loads(file.read_text(), object_pairs_hook=OrderedDict)
