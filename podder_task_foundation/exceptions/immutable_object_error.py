from typing import Optional

from .process_error import ProcessError


class ImmutableObjectError(ProcessError):
    default_how_to_solve = 'You should not update this object and try other ways'
    default_reference_url = ''

    def __init__(self, how_to_solve: Optional[str] = None, reference_url: Optional[str] = None):
        message = 'This object is immutable'
        self.message = message
        self.detail = "You can not set new value or update existing value to the immutable object"
        self.how_to_solve = how_to_solve or self.default_how_to_solve
        self.reference_url = reference_url or self.default_reference_url
        Exception.__init__(self, self.message, self.how_to_solve, self.default_reference_url)
