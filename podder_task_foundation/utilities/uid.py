import ulid


class UID(object):

    @classmethod
    def generate(cls) -> str:
        return ulid.new().str
