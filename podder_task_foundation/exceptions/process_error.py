class ProcessError(Exception):
    default_message = ''
    default_how_to_solve = ''
    default_reference_url = ''

    def __init__(self,
                 message: str = '',
                 detail: str = "",
                 how_to_solve: str = '',
                 reference_url: str = '',
                 code: str = ''):
        Exception.__init__(self, message)
        self.message = message or self.default_message
        self.detail = detail
        self.how_to_solve = how_to_solve or self.default_how_to_solve
        self.reference_url = reference_url or self.default_reference_url
        self.code = code

    @property
    def full_message(self):
        message = self.message + ':' + self.detail
        if self.how_to_solve is not None and self.how_to_solve != '':
            message = message + ':' + self.how_to_solve
        if self.reference_url is not None and self.reference_url != '':
            message = message + ':Reference Url:' + self.reference_url

        return message
