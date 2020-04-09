import re
import sys

SLUG_REGEX = r'^[a-zA-Z][-a-zA-Z0-9]+$'
MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

project_slug = '{{ cookiecutter.project_slug }}'
module_name = '{{ cookiecutter.module_name }}'

if not re.match(SLUG_REGEX, project_slug):
    print(f"ERROR: {project_slug} is not a valid slug! It may only consist of numbers and letters "
          f"of the english alphabet and it must use dashes instead of whitespace.")
    sys.exit(1)

if not re.match(MODULE_REGEX, module_name):
    print(f"ERROR: {module_name} is not a valid Python module name! "
          f"See https://www.python.org/dev/peps/pep-0008/#package-and-module-names "
          f"for naming standards.")
    sys.exit(1)
