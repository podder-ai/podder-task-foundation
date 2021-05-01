import re
import secrets
import string


class Strings(object):
    _source = string.ascii_letters + string.digits

    def random_string(self, length: int) -> str:
        return ''.join(secrets.choice(self._source) for i in range(length))

    @staticmethod
    def camel_case(source: str, title: bool = False):
        if title:
            return ''.join(x.title() for x in source.split('_'))
        else:
            return re.sub("_(.)", lambda m: m.group(1).upper(), source.lower())
