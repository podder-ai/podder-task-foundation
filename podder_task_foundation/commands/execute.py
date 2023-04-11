import re
import shutil
from argparse import Namespace
from pathlib import Path
from typing import Dict, Union

from ..bootstrap import bootstrap
from ..mode import MODE
from ..parameters import Parameters
from ..process_executor import ProcessExecutor
from .command import Command


class Execute(Command):
    name = "execute"
    aliases = ["exec"]
    help = "Execute process"

    def set_arguments(self, parser):
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
                            help='Config file path')
        parser.add_argument('-w',
                            '--overwrite',
                            dest='overwrite',
                            action='store_true',
                            help='Overwrite output file even if the files already exist')
        parser.add_argument('-p',
                            '--pretty',
                            dest='pretty',
                            action='store_true',
                            help='Pretty print output ons json output')

    def handler(self, arguments: Namespace, unknown_arguments: Parameters, *args):
        process_executor = ProcessExecutor(mode=MODE.CONSOLE,
                                           config_path=arguments.config,
                                           verbose=arguments.verbose,
                                           debug_mode=arguments.debug,
                                           parameters=unknown_arguments)
        bootstrap(process_executor.context)

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
        unknown_arguments.extend(vars(arguments))
        output = process_executor.execute(process_name,
                                          input_payload=_input,
                                          parameters=unknown_arguments)

        data = output.all()
        indent = None
        if arguments.pretty:
            indent = 4
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
                    file_path: Path = _object.get_file_name(base_path=output_path)
                    if file_path.exists():
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                    _object.save(path=file_path, indent=indent)
                    if arguments.verbose:
                        process_executor.context.logger.info("Save output {} to file:{}".format(
                            _object.name, file_path))
            else:
                keys = list(output_paths.keys())
                if len(keys) == 1 and keys[0] == process_executor.no_name_key and len(data) == 1:
                    file_path = output_paths[keys[0]]
                    if file_path.exists():
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                    data[0].save(file_path, indent=indent)
                    if arguments.verbose:
                        process_executor.context.logger.info("Save output {} to file:{}".format(
                            data[0].name, output_paths[keys[0]]))

                else:
                    for key in keys:
                        output_data = output.get(key)
                        if output_data is None:
                            raise Exception("Output named {} doesn't exist".format(key))
                        file_path = output_paths[key]
                        if file_path.exists():
                            if file_path.is_dir():
                                shutil.rmtree(file_path)
                            else:
                                file_path.unlink()
                        output_data.save(file_path, indent=indent)
                        if arguments.verbose:
                            process_executor.context.logger.info("Save output {} to file:{}".format(
                                output_data.name, file_path))

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
                if not overwrite:
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
