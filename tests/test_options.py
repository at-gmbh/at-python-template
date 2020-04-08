from .util import check_project


def test_base():
    check_project(run_pytest=True)


def test_pip():
    check_project(
        settings={'package_manager': 'pip'},
        files_existent=['requirements.txt', 'requirements-dev.txt'],
        files_non_existent=['environment.yml', 'environment-dev.yml'])


def test_conda():
    check_project(
        settings={'package_manager': 'conda'},
        files_existent=['environment.yml', 'environment-dev.yml'])


def test_docker():
    check_project(
        settings={'use_docker': 'yes'},
        files_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])
