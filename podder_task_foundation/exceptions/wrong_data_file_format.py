from .process_error import ProcessError


class WrongDataFormatError(ProcessError):
    default_how_to_solve = \
        'Fix data format'
    default_reference_url = ''

    def __init__(self, detail: str = "", how_to_solve: str = "", reference_url: str = ""):
        message = "Data format is wrong"
        self.message = message
        self.detail = detail or ""
        self.how_to_solve = how_to_solve or self.default_how_to_solve
        self.reference_url = reference_url or self.default_reference_url
        Exception.__init__(self, self.message, self.detail, self.how_to_solve,
                           self.default_reference_url)
