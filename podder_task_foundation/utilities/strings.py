import secrets
import string


class Strings(object):
    _source = string.ascii_letters + string.digits

    def random_string(self, length: int) -> str:
        return ''.join(secrets.choice(self._source) for i in range(length))
