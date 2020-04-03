import os
import sys

files_docker = ['Dockerfile', 'docker-compose.yml', '.dockerignore']


def handle_package_manager():
    # TODO implement
    package_manager = "{{ cookiecutter.package_manager }}"
    print("WARNING: package_manager is not yet implemented")

    if package_manager == 'conda':
        pass
    elif package_manager == 'pip':
        pass
    else:
        print(f"Error: unsupported package manager {package_manager}")
        sys.exit(1)


def handle_notebooks():
    # TODO implement
    use_notebooks = "{{ cookiecutter.use_notebooks }}"
    print("WARNING: use_notebooks is not yet implemented")


def handle_docker():
    use_docker = "{{ cookiecutter.use_docker }}"
    if use_docker == 'no':
        try:
            for file in files_docker:
                os.remove(file)
        except OSError as e:
            print(f"Error: failed to remove files - {e}")
            sys.exit(1)


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


if __name__ == "__main__":
    handle_package_manager()
    handle_notebooks()
    handle_docker()
    handle_config()
    handle_formatter()
    handle_editor_settings()
