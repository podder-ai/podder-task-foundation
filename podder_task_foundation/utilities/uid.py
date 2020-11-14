import uuid
from typing import Optional

import ulid


class UID(object):
    @classmethod
    def generate(cls, source: Optional[str] = None) -> str:
        if source is None:
            value = uuid.uuid4()
            return ulid.from_uuid(value).str

        return ulid.from_randomness(source).str
