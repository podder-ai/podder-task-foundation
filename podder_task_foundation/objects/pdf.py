from .file import File


class PDF(File):
    supported_extensions = [".pdf"]
    type = "pdf"
    default_extension = ".pdf"
