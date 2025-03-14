import logging
from pathlib import Path
from typing import Union

import importlib.resources as resources
from pyhocon import ConfigTree, ConfigFactory

logger = logging.getLogger('{{ cookiecutter.module_name }}')


def get_resource_string(path: str, decode=True) -> Union[str, bytes]:
    """
    Load a package resource (i.e. a file from within this package)

    :param path: the path, starting at the root of the current module (e.g. 'res/default.conf').
           must be a string, not a Path object!
    :param decode: if true, decode the file contents as string (otherwise return bytes)
    :return: the contents of the resource file (as string or bytes)
    """
    package = __name__.split('.')[0]  # Get the top-level package name
    with resources.files(package).joinpath(path).open('rb') as f:
        s = f.read()
    return s.decode(errors='ignore') if decode else s


def load_config(config_file: Union[str, Path] = None) -> ConfigTree:
    """
    Load the config from the specified file and use it to override fields in the default config.
    If no config file is specified, only the default config is loaded.

    :param config_file: path of the config file to load
    :return: the parsed config
    """
    base_config_str = get_resource_string('res/default.conf')
    config: ConfigTree = ConfigFactory.parse_string(base_config_str)
    if config_file:
        try:
            config = ConfigFactory.parse_file(config_file).with_fallback(config)
        except FileNotFoundError as e:
            logger.warning(f"The specified config could not be loaded (using defaults): {e}")
    return config


def logging_setup(config: ConfigTree):
    """
    setup logging based on the configuration

    :param config: the parsed config tree
    """
    fmt = config.get('logging.format')
    if config.get_bool('logging.enabled'):
        level = logging._nameToLevel[config.get('logging.level').upper()]
    else:
        level = logging.NOTSET
    logging.basicConfig(format=fmt, level=logging.WARNING)
    logger.setLevel(level)
