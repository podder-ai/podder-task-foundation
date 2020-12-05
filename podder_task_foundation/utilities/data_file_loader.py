import csv
import json
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Union

import toml
import yaml

from ..exceptions import UnsupportedFileFormatError


def represent_odict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())


yaml.add_representer(OrderedDict, represent_odict)


class DataFileLoader(object):
    supported_format = {
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".csv": "csv",
    }

    def __init__(self):
        pass

    def load(self, path: Path) -> Union[Dict, List]:
        file_format = self.get_file_type(path)
        if file_format is None:
            raise UnsupportedFileFormatError(path)
        data = None
        if file_format == "json":
            data = json.loads(path.read_text(), object_pairs_hook=OrderedDict)
        elif file_format == "yaml":
            data = yaml.load(path.read_text(), Loader=yaml.SafeLoader)
        elif file_format == "toml":
            data = toml.loads(path.read_text(), _dict=OrderedDict)
        elif file_format == "csv":
            data = []
            with path.open() as file_handler:
                reader = csv.reader(file_handler)
                for row in reader:
                    data.append(row)

        return data

    def get_file_type(self, path: Path) -> Optional[str]:
        if path.suffix not in self.supported_format.keys():
            return None
        return self.supported_format[path.suffix]
