import argparse
import importlib
import re
import time
from pathlib import Path
from typing import Dict, Optional, Union

from .config import Config
from .context import Context
from .mode import MODE
from .payload import Payload
from .pipeline import Pipeline
from .utilities import Strings


class CLI(object):
    _NO_NAME_PREFIX = "NO_NAME_"

    def __init__(self):
        self._parser = self._get_parser()
        self._no_name_key = self._NO_NAME_PREFIX + Strings().random_string(10)

    @staticmethod
    def _get_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Podder Task CLI Argument Parser')
        parser.add_argument('process_name',
                            nargs='?',
                            type=str,
                            help='specify process name which you want to execute')
        parser.add_argument('-i',
                            '--input',
                            nargs='+',
                            type=str,
                            help='Input files (you can pass file[s])')
        parser.add_argument('-o',
                            '--output',
                            nargs='+',
                            type=str,
                            help='Output files (you can pass file[s])')
        parser.add_argument('-v',
                            '--verbose',
                            dest='verbose',
                            action='store_true',
                            help='Set verbose mode')
        parser.add_argument('-c',
                            '--config',
                            nargs='?',
                            default="",
                            type=str,
                            help='Input files (you can pass file[s] or directory)')
        return parser

    def execute(self):
        arguments = self._parser.parse_args()

        output_files = arguments.output
        output_exists, should_output_to_directory, output_paths = self.check_output_type(
            output_files)

        _input = Payload()
        files = arguments.input
        if files is not None:
            for file in files:
                name, path = self._parse_name_and_file(file)
                if name == self._no_name_key:
                    name = path.name
                if path.is_dir():
                    _input.add_directory(directory=path)
                else:
                    _input.add_file(file=path, name=name)

        if arguments.config == "":
            config_path = Path(Config.default_path)
        else:
            config_path = Path(arguments.config)

        context = Context(mode=MODE.CONSOLE, config_path=config_path)
        start_time = time.time()
        if arguments.verbose:
            context.logger.info("Start Process: Job ID: {}".format(context.job_id))

        process_name = arguments.process_name
        if process_name is not None:
            output = self._execute_single_process(process_name,
                                                  _input,
                                                  config_path=config_path,
                                                  job_id=context.job_id)
        else:
            output = self._execute_pipeline(_input, config_path=config_path, job_id=context.job_id)

        data = output.all()
        if output_exists:
            if should_output_to_directory:
                keys = list(output_paths.keys())
                output_path = output_paths[keys[0]]
                if not output_path.exists():
                    output_path.mkdir(mode=0o666, parents=True)
                    if arguments.verbose:
                        context.logger.info("Created directory: {}".format(output_path))
                for _object in data:
                    file_path = _object.get_file_name(base_path=output_path)
                    _object.save(path=file_path)
                    if arguments.verbose:
                        context.logger.info("Save output {} to file:{}".format(
                            _object.name, file_path))
            else:
                keys = list(output_paths.keys())
                if len(keys) == 1 and keys[0] == self._no_name_key and len(data) == 1:
                    data[0].save(output_paths[keys[0]])
                    if arguments.verbose:
                        context.logger.info("Save output {} to file:{}".format(
                            data[0].name, output_paths[keys[0]]))

                else:
                    for key in keys:
                        output_data = output.get(key)
                        if output_data is None:
                            raise Exception("Output named {} doesn't exist".format(key))
                        output_data.save(output_paths[key])
                        if arguments.verbose:
                            context.logger.info("Save output {} to file:{}".format(
                                output_data.name, output_paths[key]))

        else:
            if arguments.verbose:
                context.logger.info("No output file specified")

        process_time = str(round((time.time() - start_time), 3))
        if arguments.verbose:
            context.logger.info("Process completed: It takes {} second(s).".format(process_time))

    def check_output_type(self, output_names: [str]) -> (bool, bool, Union[None, Dict[str, Path]]):
        if output_names is None or len(output_names) == 0:
            return False, False, None

        if len(output_names) == 1:
            output_name = output_names[0]
            name, output_path = self._parse_name_and_file(output_name)
            if output_path.exists():
                if output_path.is_dir():
                    return True, True, {name: output_path}
                else:
                    raise Exception("Output file {} already exists.".format(output_path))

            if output_path.suffix == "":
                return True, True, {name: output_path}

            return True, False, {name: output_path}

        files: Dict[str, Path] = {}
        for output_name in output_names:
            name, output_path = self._parse_name_and_file(output_name)
            if output_path.exists():
                if output_path.is_dir():
                    raise Exception(
                        "Output path {} is a directory. you cannot specify directory when you set multiple outputs"
                        .format(output_path))
                else:
                    raise Exception("Output file {} already exists.".format(output_path))

            if name == self._no_name_key:
                raise Exception(
                    "You need to specify output name ( name:path ) for file {}".format(output_path))

            if name in files:
                raise Exception("You specified output name {} more than once.".format(name))

            files[name] = output_path

        return True, False, files

    @staticmethod
    def _execute_single_process(name: str,
                                _input: Payload,
                                config_path: Path,
                                job_id: Optional[str] = None) -> Payload:
        context = Context(mode=MODE.CONSOLE,
                          process_name=name,
                          config_path=config_path,
                          job_id=job_id)
        process_module = importlib.import_module('processes.{}.process'.format(name))
        process = process_module.Process(mode=MODE.CONSOLE, context=context)

        output: Payload = process.handle(_input)
        return output

    @staticmethod
    def _execute_pipeline(_input: Payload, config_path: Path, job_id: Optional[str]) -> Payload:
        context = Context(mode=MODE.CONSOLE, config_path=config_path, job_id=job_id)
        blueprint = context.config.get("pipeline", default=None)
        pipeline = Pipeline(blueprint=blueprint, context=context)

        return pipeline.execute(_input)

    def _parse_name_and_file(self, value: str) -> (str, Path):
        matches = re.match(r"^([^=]+)=(.+)$", value)
        if matches:
            name = matches[1]
            path = Path(matches[2])
        else:
            path = Path(value)
            name = self._no_name_key

        return name, path.expanduser()
