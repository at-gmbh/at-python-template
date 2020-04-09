import argparse
import sys

from {{ cookiecutter.module_name }} import __version__{% if cookiecutter.config_file != 'none' %}
from {{ cookiecutter.module_name }} import util{% endif %}


def main():
    args = parse_args(){% if cookiecutter.config_file == 'hocon' %}
    config = util.load_config(args.config)
    util.logging_setup(config){% elif cookiecutter.config_file == 'yaml' %}
    if args.config:
        config = util.load_config(args.config)
        util.logging_setup(config){% endif %}
    # TODO your journey starts here


def parse_args() -> argparse.Namespace:
    """
    Specifies the command line argument parser using the builtin argparse module and parses
    the command line args that were given to this application (if any).

    There are two exceptions to this behaviour:

    * --version: prints the current program version and exits
    * --help: prints usage instructions and exits (argparse default behaviour)

    :return: a Namespace object that contains the parsed command line args.
             Note: the program will exit, if the --version or --help flag is specified.
    """
    # define the available command line arguments
    ap = argparse.ArgumentParser(description="{{ cookiecutter.project_name }}")
    ap.add_argument('-v', '--version', action='store_true',
                    help="prints the current program version and exits"){% if cookiecutter.config_file != 'none' %}
    ap.add_argument('-c', '--config', metavar='CONFIG', type=str, required=False,
                    help="path to the program configuration"){% endif %}
    # parse the command line arguments
    args = ap.parse_args()
    # handle the --version flag
    if args.version:
        print('{{ cookiecutter.project_slug }} ' + __version__)
        sys.exit(0)
    # return the parsed command line args
    return args
