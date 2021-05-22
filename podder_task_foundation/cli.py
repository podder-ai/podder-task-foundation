import argparse
import re
from pathlib import Path
from typing import Dict, Union

from .command_executor import CommandExecutor
from .mode import MODE
from .process_executor import ProcessExecutor


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
        parser.add_argument('-x',
                            '--command',
                            nargs='?',
                            type=str,
                            help='specify command name which you want to execute')
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
        parser.add_argument('-d',
                            '--debug',
                            dest='debug',
                            action='store_true',
                            help='Enable debug mode')
        parser.add_argument('-c',
                            '--config',
                            nargs='?',
                            default="",
                            type=str,
                            help='Input files (you can pass file[s] or directory)')
        parser.add_argument('-w',
                            '--overwrite',
                            dest='overwrite',
                            action='store_true',
                            help='Overwrite output file even if the files already exist')
        return parser

    def execute(self):
        arguments = self._parser.parse_args()

        if arguments.command is not None:
            command_executor = CommandExecutor(mode=MODE.CONSOLE,
                                               config_path=arguments.config,
                                               verbose=arguments.verbose,
                                               debug_mode=arguments.debug)
            command_executor.execute(command_name=arguments.command)
            return

        process_executor = ProcessExecutor(mode=MODE.CONSOLE,
                                           config_path=arguments.config,
                                           verbose=arguments.verbose,
                                           debug_mode=arguments.debug)

        output_files = arguments.output
        output_exists, should_output_to_directory, output_paths = self.check_output_type(
            output_files, no_name_key=process_executor.no_name_key, overwrite=arguments.overwrite)

        _input_files = []
        files = arguments.input
        if files is not None:
            for file in files:
                name, path = self._parse_name_and_file(file,
                                                       no_name_key=process_executor.no_name_key)
                if name == process_executor.no_name_key:
                    name = path.name
                _input_files.append((name, path))
        _input = process_executor.build_payload_from_files(_input_files)

        process_name = arguments.process_name
        output = process_executor.execute(
            process_name,
            input_payload=_input,
        )

        data = output.all()
        if output_exists:
            if should_output_to_directory:
                keys = list(output_paths.keys())
                output_path = output_paths[keys[0]]
                if not output_path.exists():
                    output_path.mkdir(mode=0o666, parents=True)
                    if arguments.verbose:
                        process_executor.context.logger.info(
                            "Created directory: {}".format(output_path))
                for _object in data:
                    file_path = _object.get_file_name(base_path=output_path)
                    _object.save(path=file_path)
                    if arguments.verbose:
                        process_executor.context.logger.info("Save output {} to file:{}".format(
                            _object.name, file_path))
            else:
                keys = list(output_paths.keys())
                if len(keys) == 1 and keys[0] == process_executor.no_name_key and len(data) == 1:
                    data[0].save(output_paths[keys[0]])
                    if arguments.verbose:
                        process_executor.context.logger.info("Save output {} to file:{}".format(
                            data[0].name, output_paths[keys[0]]))

                else:
                    for key in keys:
                        output_data = output.get(key)
                        if output_data is None:
                            raise Exception("Output named {} doesn't exist".format(key))
                        output_data.save(output_paths[key])
                        if arguments.verbose:
                            process_executor.context.logger.info("Save output {} to file:{}".format(
                                output_data.name, output_paths[key]))

        else:
            if arguments.verbose:
                process_executor.context.logger.info("No output file specified")

    def check_output_type(self,
                          output_names: [str],
                          no_name_key: str,
                          overwrite: bool = False) -> (bool, bool, Union[None, Dict[str, Path]]):
        if output_names is None or len(output_names) == 0:
            return False, False, None

        if len(output_names) == 1:
            output_name = output_names[0]
            name, output_path = self._parse_name_and_file(output_name, no_name_key=no_name_key)
            if output_path.exists():
                if output_path.is_dir():
                    return True, True, {name: output_path}
                elif not overwrite:
                    raise Exception("Output file {} already exists.".format(output_path))

            if output_path.suffix == "":
                return True, True, {name: output_path}

            return True, False, {name: output_path}

        files: Dict[str, Path] = {}
        for output_name in output_names:
            name, output_path = self._parse_name_and_file(output_name, no_name_key=no_name_key)
            if output_path.exists():
                if output_path.is_dir():
                    raise Exception(
                        "Output path {} is a directory. you cannot specify directory when you set multiple outputs"
                        .format(output_path))
                elif not overwrite:
                    raise Exception("Output file {} already exists.".format(output_path))

            if name == no_name_key:
                raise Exception(
                    "You need to specify output name ( name:path ) for file {}".format(output_path))

            if name in files:
                raise Exception("You specified output name {} more than once.".format(name))

            files[name] = output_path

        return True, False, files

    @staticmethod
    def _parse_name_and_file(value: str, no_name_key: str) -> (str, Path):
        matches = re.match(r"^([^=]+)=(.+)$", value)
        if matches:
            name = matches[1]
            path = Path(matches[2])
        else:
            path = Path(value)
            name = no_name_key

        return name, path.expanduser()
