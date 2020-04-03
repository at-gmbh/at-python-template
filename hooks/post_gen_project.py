import os
import sys

files_docker = ['Dockerfile', 'docker-compose.yml', '.dockerignore']


def handle_docker():
    use_docker = "{{ cookiecutter.use_docker }}"
    if use_docker == 'no':
        try:
            for file in files_docker:
                os.remove(file)
        except OSError as e:
            print(f"Error: failed to remove files - {e}")
            sys.exit(1)


if __name__ == "__main__":
    handle_docker()
