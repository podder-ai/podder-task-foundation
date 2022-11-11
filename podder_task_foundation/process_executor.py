import importlib
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

from .config import Config
from .context import Context
from .mode import MODE
from .parameters import Parameters
from .payload import Payload
from .pipeline import Pipeline
from .utilities import Strings


class ProcessExecutor(object):
    _NO_NAME_PREFIX = "NO_NAME_"

    def __init__(self,
                 config_path: Optional[str],
                 mode: str = MODE.CONSOLE,
                 verbose: bool = False,
                 debug_mode: bool = False,
                 parameters: Optional[Parameters] = None):
        self._no_name_key = self._NO_NAME_PREFIX + Strings().random_string(10)
        if config_path is None or config_path == "":
            config_path_object = Path(Config.default_path)
        else:
            config_path_object = Path(config_path)

        self._context = Context(mode=mode,
                                config_path=config_path_object,
                                debug_mode=debug_mode,
                                verbose=verbose,
                                parameters=parameters)

    @property
    def context(self) -> Context:
        return self._context

    @property
    def no_name_key(self) -> str:
        return self._no_name_key

    def execute(self,
                process_name: Optional[str],
                input_payload: Payload,
                parameters: Parameters = None) -> Payload:

        start_time = time.time()

        if self._context.debug_mode:
            self._context.logger.debug("Debug mode enabled")

        if self._context.verbose:
            self._context.logger.info("Start Process: Job ID: {}".format(self._context.job_id))

        if process_name is not None:
            output = self._execute_single_process(name=process_name,
                                                  _input=input_payload,
                                                  parameters=parameters)
        else:
            output = self._execute_pipeline(_input=input_payload, parameters=parameters)

        process_time = str(round((time.time() - start_time), 3))
        if self._context.verbose:
            self._context.logger.info(
                "Process completed: It takes {} second(s).".format(process_time))

        return output

    def _execute_single_process(self,
                                name: str,
                                _input: Payload,
                                parameters: Parameters = None) -> Payload:
        context = Context.copy(process_name=name,
                               parameters=parameters,
                               logger=self.context.logger,
                               original=self.context)
        process_module = importlib.import_module('processes.{}.process'.format(name))
        process = process_module.Process(mode=self._context.mode, context=context)

        output: Payload = process.handle(_input)
        return output

    def _execute_pipeline(self, _input: Payload, parameters: Parameters = None) -> Payload:
        context = Context.copy(process_name=None,
                               parameters=parameters,
                               logger=self.context.logger,
                               original=self.context)
        blueprint = context.config.get("pipeline", default=None)
        pipeline = Pipeline(blueprint=blueprint, context=context)

        return pipeline.execute(_input)

    @staticmethod
    def build_payload_from_files(files: [Tuple[str, Path]]) -> Payload:
        _input = Payload()
        for name, path in files:
            if path.is_dir():
                _input.add_directory(directory=path, name=name)
            else:
                _input.add_file(file=path, name=name)

        return _input

    def store_payload_to_files(self,
                               payload: Payload,
                               output_paths: Dict[str, Path],
                               should_output_to_directory: bool = False):
        data = payload.all()
        if should_output_to_directory:
            keys = list(output_paths.keys())
            output_path = output_paths[keys[0]]
            if not output_path.exists():
                output_path.mkdir(mode=0o666, parents=True)
                if self._context.verbose:
                    self._context.logger.info("Created directory: {}".format(output_path))
                for _object in data:
                    file_path = _object.get_file_name(base_path=output_path)
                    _object.save(path=file_path)
                    if self._context.verbose:
                        self._context.logger.info("Save output {} to file:{}".format(
                            _object.name, file_path))
            else:
                keys = list(output_paths.keys())
                if len(keys) == 1 and keys[0] == self._no_name_key and len(data) == 1:
                    data[0].save(output_paths[keys[0]])
                    if self._context.verbose:
                        self._context.logger.info("Save output {} to file:{}".format(
                            data[0].name, output_paths[keys[0]]))

                else:
                    for key in keys:
                        output_data = payload.get(key)
                        if output_data is None:
                            raise Exception("Output named {} doesn't exist".format(key))
                        output_data.save(output_paths[key])
                        if self._context.verbose:
                            self._context.logger.info("Save output {} to file:{}".format(
                                output_data.name, output_paths[key]))
