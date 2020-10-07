import platform
import re
import sys
from distutils.version import StrictVersion

import cookiecutter

# check Python version (3.6 or higher)
if sys.version_info < (3, 6):
    print("ERROR: You are using Python {}, but Python 3.6 or higher is required "
          "to use this template".format(platform.python_version()))
    sys.exit(1)

# check cookiecutter version (1.7.2 or higher)
if StrictVersion(cookiecutter.__version__) < StrictVersion('1.7.2'):
    print("ERROR: You are using cookiecutter {}, but cookiecutter 1.7.2 or higher is required "
          "to use this template".format(cookiecutter.__version__))
    sys.exit(1)

# check the slug and module name
SLUG_REGEX = r'^[a-zA-Z][-a-zA-Z0-9]+$'
MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

project_slug = '{{ cookiecutter.project_slug }}'
module_name = '{{ cookiecutter.module_name }}'

if not re.match(SLUG_REGEX, project_slug):
    print(f"ERROR: {project_slug} is not a valid slug! It may only consist of numbers and letters "
          f"of the english alphabet, begin with a letter, and must use dashes instead of whitespace.")
    sys.exit(1)

if not re.match(MODULE_REGEX, module_name):
    print(f"ERROR: {module_name} is not a valid Python module name! "
          f"See https://www.python.org/dev/peps/pep-0008/#package-and-module-names "
          f"for naming standards.")
    sys.exit(1)
