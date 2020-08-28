import os
import shutil
import sys
from glob import glob
from pathlib import Path
from typing import Iterable, Optional

module_dir = 'src/{{ cookiecutter.module_name }}'
files_pip = [
    'requirements.txt',
    'requirements-dev.txt',
]
files_conda = [
    'environment.yml',
    'environment-dev.yml',
]
files_docker_aux = [
    'docker-compose.yml',
    '.dockerignore',
]

files_dockerfile_pip = [
    'Dockerfile__pip',
]

files_dockerfile_conda = [
    'Dockerfile__conda',
]
files_cli = [
    f'{module_dir}/__main__.py',
    f'{module_dir}/main__cli.py',
]
files_config_yaml = [
    f'{module_dir}/util__yaml.py',
    'config/config.yml',
]
files_config_hocon = [
    f'{module_dir}/util__hocon.py',
    f'{module_dir}/res/default.conf',
    'config/debug.conf',
]
folders_editor = [
    '.idea__editor',
    '.vscode__editor',
]


def handle_package_manager():
    package_manager = '{{ cookiecutter.package_manager }}'
    if package_manager == 'conda':
        _delete_files(files_pip)
    elif package_manager == 'pip':
        _delete_files(files_conda)
    else:
        print(f"Error: unsupported package manager {package_manager}")
        sys.exit(1)


def handle_notebooks():
    use_notebooks = '{{ cookiecutter.use_notebooks }}'
    if use_notebooks == 'no':
        shutil.rmtree('notebooks')


def handle_docker():
    use_docker = '{{ cookiecutter.use_docker }}'
    if use_docker == 'no':
        _delete_files(files_docker_aux + files_dockerfile_pip + files_dockerfile_conda)
    else:
        package_manager = '{{ cookiecutter.package_manager }}'
        if package_manager == "conda":
            _delete_files(files_dockerfile_pip)
            _rename_files("Dockerfile__conda", "__conda", "")
        elif package_manager == "pip":
            _delete_files(files_dockerfile_conda)
            _rename_files("Dockerfile__pip", "__pip", "")


def handle_cli():
    create_cli = '{{ cookiecutter.create_cli }}'
    if create_cli == 'yes':
        _delete_files([f'{module_dir}/main.py'])
        _rename_files('src/**/*__cli.py', '__cli', '')
    else:
        _delete_files(files_cli)


def handle_config():
    config_file = '{{ cookiecutter.config_file }}'
    if config_file == 'yaml':
        _delete_files(files_config_hocon)
        shutil.rmtree(f'{module_dir}/res')
        _rename_files(f'src/**/*__yaml.py', '__yaml', '')
    elif config_file == 'hocon':
        _delete_files(files_config_yaml)
        _rename_files(f'src/**/*__hocon.py', '__hocon', '')
    else:
        _delete_files(files_config_hocon + files_config_yaml + ['tests/test_util.py'])
        os.rmdir(f'{module_dir}/res')
        os.rmdir('config')


def handle_formatter():
    code_formatter = '{{ cookiecutter.code_formatter }}'
    if code_formatter in ['none', 'black']:
        # no action necessary
        pass
    else:
        print(f"Error: unsupported formatter {code_formatter}")
        sys.exit(1)


def handle_editor_settings():
    editor_settings = '{{ cookiecutter.editor_settings }}'
    if editor_settings == 'vscode':
        _rename_files('.vscode__editor', '__editor', '')
        _delete_folders(folders_editor, exclude='.vscode')
    elif editor_settings == 'pycharm':
        _rename_files('.idea__editor', '__editor', '')
        _delete_folders(folders_editor, exclude='.idea')
    elif editor_settings == 'none':
        _delete_folders(folders_editor)
    else:
        print(f"Error: unsupported editor {editor_settings}")
        sys.exit(1)


def print_success():
    full_name = '{{ cookiecutter.full_name }}'
    print(f"Hey {full_name}! Your project was successfully created at {os.getcwd()}. "
          f"Have fun with it!")


def _rename_files(file_pattern, old, new):
    for file in glob(file_pattern, recursive=True):
        path = Path(file)
        path.rename(path.with_name(path.name.replace(old, new)))


def _delete_files(files: Iterable[str], exclude: Optional[str] = None):
    try:
        for file in files:
            if file != exclude:
                os.remove(file)
    except OSError as e:
        print(f"Error: failed to remove files - {e}")
        sys.exit(1)


def _delete_folders(folders: Iterable[str], exclude: Optional[str] = None):
    for folder in folders:
        if folder != exclude:
            shutil.rmtree(folder, ignore_errors=True)


if __name__ == '__main__':
    handle_package_manager()
    handle_cli()
    handle_notebooks()
    handle_docker()
    handle_config()
    handle_formatter()
    handle_editor_settings()
    print_success()
