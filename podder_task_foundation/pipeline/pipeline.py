import importlib
from typing import List, Optional, Union

from ..context import Context
from ..exceptions import DataFormatError, ProcessError
from ..payload import Payload
from ..process import Process
from .job import Job
from .pipe import Pipe


class Pipeline(object):

    def __init__(self, blueprint: dict, context: Context):
        self._blueprint: dict = blueprint
        self._pipeline: Optional[Pipe] = None
        self._context = context
        self._process_cache = {}
        self.load()

    def load(self):
        self._pipeline = self._build_pipeline(self._blueprint)

    def execute(self, _input: Payload) -> Payload:
        if self._pipeline is None:
            raise ProcessError(
                message="Pipeline is not loaded yet",
                detail="Pipeline is None because it is not loaded yet",
                how_to_solve="You need to use load method to load pipeline befor you execute it.",
                reference_url="")
        return self._pipeline.execute(_input)

    def _build_pipeline(self, blueprint: dict) -> Pipe:
        if Pipe.Type.SERIAL in blueprint and Pipe.Type.PARALLEL in blueprint:
            raise DataFormatError(detail="Pipeline data include \"parallel\" and \"serial\" both",
                                  how_to_solve="Check your pipeline config and fix the format.",
                                  reference_url="")

        if Pipe.Type.SERIAL in blueprint:
            _type = Pipe.Type.SERIAL
        elif Pipe.Type.PARALLEL in blueprint:
            _type = Pipe.Type.PARALLEL
        else:
            raise DataFormatError(detail="Pipeline data does't include \"parallel\" or \"serial\"",
                                  how_to_solve="Check your pipeline config and fix the format.",
                                  reference_url="")
        units = []
        for name in blueprint[_type]:
            if isinstance(name, str):
                job = Job(self._get_process(name))
                units.append(job)
            else:
                pipe = self._build_pipeline(blueprint=name)
                units.append(pipe)

        return Pipe(units=units, execute_type=_type)

    def _get_process(self, name: str) -> Process:
        if name in self._process_cache:
            return self._process_cache[name]
        logger = None
        if self._context.is_process_context:
            logger = self._context.logger

        context = Context.copy(process_name=name,
                               parameters=None,
                               logger=logger,
                               original=self._context)
        process_module = importlib.import_module('processes.{}.process'.format(name))
        process = process_module.Process(mode=self._context.mode, context=context)
        self._process_cache[name] = process

        return process

    @classmethod
    def execute_process(cls, process_name: Union[str, List[str]], input_payload: Payload,
                        context: Context) -> Payload:
        if type(process_name) == str:
            process_name = [process_name]
        pipeline = Pipeline(blueprint={"serial": process_name}, context=context)
        return pipeline.execute(_input=input_payload)
