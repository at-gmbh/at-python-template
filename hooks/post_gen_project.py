import os
import shutil
import sys
from glob import glob
from pathlib import Path

module_dir = "src/{{ cookiecutter.module_name }}"
files_pip = [
    "requirements.txt",
    "requirements-dev.txt",
]
files_conda = [
    "environment.yml",
    "environment-dev.yml",
]
files_docker = [
    "Dockerfile",
    "docker-compose.yml",
    ".dockerignore",
]
files_config_yaml = [
    f"{module_dir}/util__yaml.py",
    "config/config.yml",
]
files_config_hocon = [
    f"{module_dir}/util__hocon.py",
    f"{module_dir}/res/default.conf",
    "config/debug.conf",
]


def handle_package_manager():
    package_manager = "{{ cookiecutter.package_manager }}"
    if package_manager == "conda":
        _delete_files(files_pip)
    elif package_manager == "pip":
        _delete_files(files_conda)
    else:
        print(f"Error: unsupported package manager {package_manager}")
        sys.exit(1)


def handle_notebooks():
    use_notebooks = "{{ cookiecutter.use_notebooks }}"
    if use_notebooks == "no":
        shutil.rmtree("notebooks", ignore_errors=True)


def handle_docker():
    use_docker = "{{ cookiecutter.use_docker }}"
    if use_docker == "no":
        _delete_files(files_docker)


def handle_config():
    config_file = "{{ cookiecutter.config_file }}"
    if config_file == "yaml":
        print("WARNING: yaml config is not yet implemented")
        _delete_files(files_config_hocon)
        _rename_files(f"src/**/*__yaml.py", "__yaml", "")
    elif config_file == "hocon":
        _delete_files(files_config_yaml)
        _rename_files(f"src/**/*__hocon.py", "__hocon", "")
    else:
        shutil.rmtree(f"{module_dir}/res")
        shutil.rmtree("config")


def handle_formatter():
    # TODO implement
    code_formatter = "{{ cookiecutter.code_formatter }}"
    print("WARNING: code_formatter is not yet implemented")


def handle_editor_settings():
    # TODO implement
    editor_settings = "{{ cookiecutter.editor_settings }}"
    print("WARNING: editor_settings is not yet implemented")


def print_success():
    full_name = "{{ cookiecutter.full_name }}"
    print(f"Hey {full_name}! Your project was successfully created at {os.getcwd()}. "
          f"Have fun with it!")


def _rename_files(file_pattern, old, new):
    for file in glob(file_pattern, recursive=True):
        path = Path(file)
        path.rename(path.with_name(path.name.replace(old, new)))


def _delete_files(files):
    try:
        for file in files:
            os.remove(file)
    except OSError as e:
        print(f"Error: failed to remove files - {e}")
        sys.exit(1)


if __name__ == "__main__":
    handle_package_manager()
    handle_notebooks()
    handle_docker()
    handle_config()
    handle_formatter()
    handle_editor_settings()
    print_success()
