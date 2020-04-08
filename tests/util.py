import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Dict, List

from cookiecutter.main import cookiecutter

root = str(Path(__file__).parent.parent)

expected_files_base = [
    '.editorconfig',
    '.gitignore',
    '.pre-commit-config.yaml',
    'README.md',
    'setup.py',
    #'tests/__init__.py',
    'src/{module_name}/__init__.py',
    'src/{module_name}/__main__.py',
    'src/{module_name}/cli.py',
    'src/{module_name}/version.py',
]


def resolve_module_dir(project_dir: Path, files: List[str]) -> List[str]:
    # get the module name and replace it in the file paths, if specified
    module_name = os.listdir(project_dir / 'src')[0]
    assert (project_dir / 'src' / module_name).is_dir()
    return [s.format(module_name=module_name) if '{' in s else s for s in files]


def check_files(project_dir: Path, files: List[str], exist=True):
    for file in files:
        path = (project_dir / file).resolve()
        assert path.exists() == exist, f"file '{path}' should {'' if exist else 'not '}have existed"


def check_project(
        project_name="Test Project", settings: Dict[str, str] = None, files_existent: List = None,
        files_non_existent: List = None, run_pytest=False, fun: Callable[[Path], None] = None):
    # define cookiecutter settings
    if settings is None:
        settings = {'project_name': project_name}
    else:
        settings['project_name'] = project_name
    # work in a new temporary directory
    with TemporaryDirectory() as temp_dir:
        # create the project files from the cookiecutter template
        project_dir = cookiecutter(root, extra_context=settings, no_input=True, output_dir=temp_dir)
        project_dir = Path(project_dir)
        # check that certain files exist
        paths_pos = resolve_module_dir(project_dir, expected_files_base + (files_existent or []))
        check_files(project_dir, paths_pos)
        # check that certain other files do NOT exist
        if files_non_existent:
            paths_neg = resolve_module_dir(project_dir, files_non_existent)
            check_files(project_dir, paths_neg, exist=False)
        # run pytests, if specified
        if run_pytest:
            src_dir = str(project_dir / 'src')
            result = subprocess.run([sys.executable, '-m', 'pytest', '..'], cwd=src_dir)
            assert result.returncode == 0, "some pytest cases had errors"
        # run additional code, if specified
        if fun:
            fun(project_dir)
