from pathlib import Path

from .process_error import ProcessError


class DataFormatError(ProcessError):
    default_how_to_solve = ''
    default_reference_url = ''

    def __init__(self, detail, how_to_solve: str, reference_url: str):
        message = "Data Format Error"
        self.message = message
        self.detail = detail
        self.how_to_solve = how_to_solve or self.default_how_to_solve
        self.reference_url = reference_url or self.default_reference_url
        Exception.__init__(self, self.message, self.detail, self.how_to_solve,
                           self.default_reference_url)
