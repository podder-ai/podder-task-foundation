from ..payload import Payload
from ..process import Process


class Job(object):
    def __init__(self, process: Process):
        self._process = process

    def execute(self, _input: Payload) -> Payload:
        output: Payload = self._process.handle(_input)

        return output
