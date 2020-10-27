import argparse
import importlib
from pathlib import Path
from typing import Optional

from .config import Config
from .context import Context
from .mode import MODE
from .payload import Payload
from .pipeline import Pipeline


class CLI(object):
    def __init__(self):
        self._parser = self._get_parser()

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
                            help='Input files (you can pass file[s])')
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
        ok, should_output_to_directory, output_path = self.check_output_type(output_files)
        if not ok:
            return

        _input = Payload()
        files = arguments.input
        if files is not None:
            for file in files:
                path = Path(file).expanduser()
                if path.is_dir():
                    _input.add_directory(directory=path)
                else:
                    _input.add_file(file=path)

        if arguments.config == "":
            config_path = Path(Config.default_path)
        else:
            config_path = Path(arguments.config)

        process_name = arguments.process_name
        if process_name is not None:
            output = self._execute_single_process(process_name, _input, config_path=config_path)
        else:
            output = self._execute_pipeline(_input, config_path=config_path)

        data = output.all()
        if should_output_to_directory:
            if not output_path.exists():
                output_path.mkdir(mode=0o666, parents=True)
            for _object in data:
                _object.save(path=_object.get_file_name(base_path=output_path))
        else:
            if len(data) == 1:
                data[0].save(output_path)
            elif len(data) > 1:
                raise Exception(
                    "You should set directory name to the output because there are multiple outputs"
                )
            else:
                raise Exception("No output for {}".format(output_path))

    @staticmethod
    def check_output_type(output_names: [str]) -> (bool, bool, Optional[Path]):
        if output_names is None or len(output_names) == 0:
            return None
        output_name = output_names[0]
        output_path = Path(output_name).expanduser()
        if output_path.exists():
            if output_path.is_dir():
                return True, True, output_path
            else:
                raise Exception("Output file {} already exists.".format(output_path))

        if output_path.suffix == "":
            return True, True, output_path

        return True, False, output_path

    @staticmethod
    def _execute_single_process(name: str, _input: Payload, config_path: Path) -> Payload:
        process_config_path = config_path.joinpath(name)
        context = Context(mode=MODE.CONSOLE, process_name=name, config_path=process_config_path)
        process_module = importlib.import_module('processes.{}.process'.format(name))
        process = process_module.Process(mode=MODE.CONSOLE, context=context)

        output: Payload = process.handle(_input)
        return output

    @staticmethod
    def _execute_pipeline(_input: Payload, config_path: Path) -> Payload:
        context = Context(mode=MODE.CONSOLE, config_path=config_path)
        blueprint = context.config.get("pipeline", default=None)
        pipeline = Pipeline(blueprint=blueprint, context=context, mode=MODE.CONSOLE)

        return pipeline.execute(_input)
