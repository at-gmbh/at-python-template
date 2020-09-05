import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Dict, List, Union

from cookiecutter.main import cookiecutter

root = str(Path(__file__).parent.parent)

expected_files_base = [
    '.editorconfig',
    '.gitignore',
    '.pre-commit-config.yaml',
    'README.md',
    'src/{module_name}/__init__.py',
    'src/{module_name}/main.py',
    'src/{module_name}/version.py',
]


def get_module_name(project_dir: Path) -> str:
    module_name = os.listdir(project_dir / 'src')[0]
    assert (project_dir / 'src' / module_name).is_dir()
    return module_name


def resolve_module_dir(files: List[str], module_name: str) -> List[str]:
    return [(s.format(module_name=module_name) if '{' in s else s) for s in files] if files else []


def check_files(project_dir: Path, files: List[str], exist=True):
    for file in files:
        path = (project_dir / file).resolve()
        assert path.exists() == exist, f"file '{path}' should {'' if exist else 'not '}have existed"


def list_files(base_dir, indent=4):
    for base, dirs, files in os.walk(base_dir):
        level = len(Path(base).relative_to(base_dir).parents)
        space = ' ' * indent * level
        print('{}{}/'.format(space, os.path.basename(base)))
        space_sub = ' ' * indent * (level + 1)
        for f in files:
            print('{}{}'.format(space_sub, f))


def check_project(
        project_name="Test Project", settings: Dict[str, str] = None, files_existent: List = None,
        files_non_existent: List = None, test_cli=False, run_pytest=False,
        fun: Callable[[Path], None] = None):
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
        module_name = get_module_name(project_dir)
        src_dir = str(project_dir / 'src')
        list_files(project_dir)
        # check that certain files exist and make sure that others do not exist
        paths_pos = resolve_module_dir(expected_files_base + (files_existent or []), module_name)
        paths_neg = resolve_module_dir(files_non_existent, module_name)
        check_files(project_dir, paths_pos)
        check_files(project_dir, paths_neg, exist=False)
        # test the CLI
        if test_cli:
            result = subprocess.run([sys.executable, '-m', module_name, '--version'], cwd=src_dir)
            assert result.returncode == 0, "cli call returned a nonzero exit code"
        # run pytests, if specified
        if run_pytest:
            result = subprocess.run([sys.executable, '-m', 'pytest', '..'], cwd=src_dir)
            assert result.returncode == 0, "some pytest cases had errors"
        # run additional code, if specified
        if fun:
            fun(project_dir)


def assert_file_contains(file: Union[str, Path], contains: str = None, not_contains: str = None):
    with open(file, 'r') as fp:
        content = fp.read()
        if contains:
            assert contains in content, f"'{contains}' should have been found in '{file}'"
        if not_contains:
            assert not_contains not in content, f"'{contains}' should not exist in '{file}'"
