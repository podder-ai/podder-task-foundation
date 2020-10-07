from pathlib import Path

from .process_error import ProcessError


class UnsupportedFileFormatError(ProcessError):
    default_how_to_solve = \
        'Change format to supported file type and use it\'s extension ( such as .yaml / .json / .toml )'
    default_reference_url = ''

    def __init__(self,
                 path: Path,
                 detail: str = "",
                 how_to_solve: str = "",
                 reference_url: str = ""):
        message = "This system doesn't support file type \"{}\"".format(
            path.suffix)
        self.message = message
        self.detail = detail or "Unsupported File Path: \"{}\"".format(
            str(path))
        self.how_to_solve = how_to_solve or self.default_how_to_solve
        self.reference_url = reference_url or self.default_reference_url
        Exception.__init__(self, self.message, self.detail, self.how_to_solve,
                           self.default_reference_url)
