import os
from pathlib import Path

from .config import Config
from .exceptions import DirectoryNotFoundError


class File(object):
    """
    File assessor
    All tasks need to access file through this class
    """
    def __init__(self, process_name: str, config: Config):
        self._process_name = process_name
        self._config = config
        self._root_path = os.path.abspath(config.get('file.root_directory', './'))

    def get_root_path(self) -> str:
        return self._root_path

    def get_input_path(self, name: str = '') -> str:
        """
        Returns absolute path to `input` directory.
        """
        directory_path = self._config.get('file.input_directory',
                                          os.path.join(self.get_root_path(), 'input'))

        directory_path_object = Path(directory_path)
        if not Path(directory_path).exists():
            raise DirectoryNotFoundError(directory_path_object,
                                         detail="Input directory should be placed on " +
                                         str(directory_path_object.resolve()),
                                         how_to_solve="Create config directory on " +
                                         str(directory_path_object.resolve()) +
                                         " or set proper path on config file",
                                         reference_url="")

        return os.path.abspath(os.path.join(directory_path, name))

    def get_output_path(self, name: str = '') -> str:
        """
        Returns absolute path to `output` directory.
        """
        directory_path = self._config.get('file.output_directory',
                                          os.path.join(self.get_root_path(), 'output'))

        directory_path_object = Path(directory_path)
        if not Path(directory_path).exists():
            raise DirectoryNotFoundError(directory_path_object,
                                         detail="Output directory should be placed on " +
                                         str(directory_path_object.resolve()),
                                         how_to_solve="Create config directory on " +
                                         str(directory_path_object.resolve()) +
                                         " or set proper path on config file",
                                         reference_url="")

        return os.path.abspath(os.path.join(directory_path, self._process_name, name))

    def get_data_path(self, name: str = '') -> str:
        """
        Returns absolute path to `data` directory.
        """
        directory_path = self._config.get('file.data_directory',
                                          os.path.join(self.get_root_path(), 'data'))

        directory_path_object = Path(directory_path)
        if not Path(directory_path).exists():
            raise DirectoryNotFoundError(
                directory_path_object,
                detail="Data directory should be placed on " + str(directory_path_object.resolve()),
                how_to_solve="Create config directory on " + str(directory_path_object.resolve()) +
                " or set proper path on config file",
                reference_url="")

        return os.path.abspath(os.path.join(directory_path, self._process_name, name))

    def get_temporary_path(self, name: str = '') -> str:
        """
        Returns absolute path to `tmp` directory.
        """
        directory_path = self._config.get('file.temporary_directory',
                                          os.path.join(self.get_root_path(), 'tmp'))

        return os.path.abspath(os.path.join(directory_path, self._process_name, name))

    def get_input_file(self, name: str) -> Path:
        path = Path(self.get_input_path(name))
        return path

    def get_data_file(self, name: str) -> Path:
        path = Path(self.get_data_path(name))
        return path

    def get_output_file(self, name: str) -> Path:
        path = Path(self.get_output_path(name))
        return path
