from ..payload import Payload
from .thread_with_return_value import ThreadWithReturnValue
from .unit import Unit


class Pipe(Unit):

    class Type:
        SERIAL = "serial"
        PARALLEL = "parallel"

    def __init__(self, units: [Unit], execute_type: str, use_thread=False):
        self._units = units
        self._type = execute_type
        self._use_thread = use_thread

    def execute(self, _input: Payload) -> Payload:
        if self._type == Pipe.Type.SERIAL:
            return self._execute_serial(_input)
        else:
            return self._execute_parallel(_input)

    def _execute_serial(self, _input: Payload) -> Payload:
        current_payload = _input
        for unit in self._units:
            current_payload = unit.execute(current_payload)
        return current_payload

    def _execute_parallel(self, _input: Payload) -> Payload:
        output = Payload()
        if self._use_thread:
            threads = []
            for unit in self._units:
                thread = ThreadWithReturnValue(target=unit.execute, args=[_input.copy()])
                thread.start()
                threads.append(thread)
            for thread in threads:
                result = thread.join()
                output.merge(result)
        else:
            for unit in self._units:
                result = unit.execute(_input.copy())
                output.merge(result)

        return output
