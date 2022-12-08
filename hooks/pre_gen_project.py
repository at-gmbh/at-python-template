"""
This file contains the Pre-Generate Hooks for Cookiecutter.
They are executed AFTER the user entered their project config,
but BEFORE the project is actually generated. More details:
https://cookiecutter.readthedocs.io/en/1.7.2/advanced/hooks.html

In this script we execute environment checks and run input validation.
Because the environment check needs to work with old Python versions (e.g. Python 2.7),
we need to avoid modern syntax features in this file, like f-strings and type hints.
"""
import platform
import re
import sys
from distutils.version import StrictVersion
import warnings

import cookiecutter

# check Python version (3.7 or higher)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    if StrictVersion(platform.python_version()) < StrictVersion("3.7.0"):
        print(
            "ERROR: You are using Python {}, but Python 3.7 or higher is required "
            "to use this template".format(platform.python_version())
        )
        sys.exit(1)
    # check cookiecutter version (1.7.2 or higher)
    if StrictVersion(cookiecutter.__version__) < StrictVersion("1.7.2"):
        print(
            "ERROR: You are using cookiecutter {}, but cookiecutter 1.7.2 or higher is required "
            "to use this template".format(cookiecutter.__version__)
        )
        sys.exit(1)

# check the slug and module name
SLUG_REGEX = r"^[a-zA-Z][-a-zA-Z0-9]+$"
MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

project_slug = "{{ cookiecutter.project_slug }}"
module_name = "{{ cookiecutter.module_name }}"

if not re.match(SLUG_REGEX, project_slug):
    print(
        "ERROR: {} is not a valid slug! It may only consist of numbers and letters of the "
        "english alphabet, begin with a letter, and must use dashes instead of whitespace.".format(
            project_slug
        )
    )
    sys.exit(1)

if not re.match(MODULE_REGEX, module_name):
    print(
        "ERROR: {} is not a valid Python module name! "
        "See https://www.python.org/dev/peps/pep-0008/#package-and-module-names "
        "for naming standards.".format(module_name)
    )
    sys.exit(1)
