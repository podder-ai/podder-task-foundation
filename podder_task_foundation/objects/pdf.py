from pathlib import Path
from typing import Optional

from .file import File


class PDF(File):
    supported_extensions = [".pdf"]
    type = "pdf"
