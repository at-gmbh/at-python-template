import logging
from typing import Union

import pkg_resources

logger = logging.getLogger('{{ cookiecutter.module_name }}')


def get_resource_string(path: str, decode=True) -> Union[str, bytes]:
    """
    Load a package resource (i.e. a file from within this package)

    :param path: the path, starting at the root of the current module (e.g. 'res/default.conf').
           must be a string, not a Path object!
    :param decode: if true, decode the file contents as string (otherwise return bytes)
    :return: the contents of the resource file (as string or bytes)
    """
    s = pkg_resources.resource_string(__name__.split('.')[0], path)
    return s.decode(errors='ignore') if decode else s
