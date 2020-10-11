import argparse
import importlib
from pathlib import Path

from .config import Config
from .context import Context
from .mode import MODE
from .payload import Payload


class CLI(object):
    def __init__(self):
        self._parser = self._get_parser()

    @staticmethod
    def _get_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Podder Task CLI Argument Parser')
        parser.add_argument('process_name',
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
        process_name = arguments.process_name
        if arguments.config == "":
            config_path = Path(Config.default_path).joinpath(process_name)
        else:
            config_path = Path(arguments.config)

        context = Context(mode=MODE.CONSOLE, process_name=process_name, config_path=config_path)
        process_module = importlib.import_module('processes.{}.process'.format(process_name))
        process = process_module.Process(mode=MODE.CONSOLE, context=context)
        _input = Payload()
        files = arguments.input
        for file in files:
            path = Path(file).expanduser()
            if path.is_dir():
                _input.add_directory(directory=path)
            else:
                _input.add_file(file=path)

        output = process.handle(_input)

        output_files = arguments.output
        if len(output_files) > 0:
            data = output.get_all_data()
            output_path = Path(output_files[0]).expanduser()
            if len(data) > 0:
                data[0].save(output_path)
            else:
                Exception("No output for {}".format(output_path))
