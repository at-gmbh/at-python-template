import logging
from pathlib import Path
from typing import Union

import importlib.resources as resources
from omegaconf import DictConfig, OmegaConf

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


def load_config(config_file: Union[str, Path]) -> DictConfig:
    """
    Load the config from the specified YAML file.

    Uses OmegaConf, which supports variable interpolation (${key}) and config
    merging on top of standard YAML. See https://omegaconf.readthedocs.io/

    :param config_file: path of the config file to load
    :return: the parsed config as a DictConfig (supports both dict and dot-notation access)
    """
    return OmegaConf.load(config_file)


def logging_setup(config: DictConfig):
    """
    Setup logging based on the configuration.

    :param config: the parsed config tree
    """
    log_conf = config.logging
    fmt = log_conf.format
    if log_conf.enabled:
        level = logging._nameToLevel[log_conf.level.upper()]
    else:
        level = logging.NOTSET
    logging.basicConfig(format=fmt, level=logging.WARNING)
    logger.setLevel(level)
