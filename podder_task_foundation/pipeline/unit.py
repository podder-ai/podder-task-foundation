from ..payload import Payload


class Unit(object):

    def execute(self, _input: Payload) -> Payload:
        raise NotImplementedError
