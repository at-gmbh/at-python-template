import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.module_name }}'

if not re.match(MODULE_REGEX, module_name):
    print(f"ERROR: {module_name} is not a valid Python module name! "
          f"See https://www.python.org/dev/peps/pep-0008/#package-and-module-names "
          f"for naming standards.")
    sys.exit(1)
