import os
import shutil
import sys

files_pip = ["requirements.txt", "requirements-dev.txt"]
files_conda = ["environment.yml", "environment-dev.yml"]
files_docker = ["Dockerfile", "docker-compose.yml", ".dockerignore"]


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
    # TODO implement
    config_file = "{{ cookiecutter.config_file }}"
    print("WARNING: config_file is not yet implemented")


def handle_formatter():
    # TODO implement
    code_formatter = "{{ cookiecutter.code_formatter }}"
    print("WARNING: code_formatter is not yet implemented")


def handle_editor_settings():
    # TODO implement
    editor_settings = "{{ cookiecutter.editor_settings }}"
    print("WARNING: editor_settings is not yet implemented")


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
