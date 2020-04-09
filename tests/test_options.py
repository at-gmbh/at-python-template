import pytest

from .util import check_project


def test_base():
    check_project(test_cli=True, run_pytest=True)


def test_pip():
    check_project(
        settings={'package_manager': 'pip'},
        files_existent=['requirements.txt', 'requirements-dev.txt'],
        files_non_existent=['environment.yml', 'environment-dev.yml'])


def test_conda():
    check_project(
        settings={'package_manager': 'conda'},
        files_existent=['environment.yml', 'environment-dev.yml'])


def test_notebooks_yes():
    check_project(
        settings={'use_notebooks': 'yes'},
        files_existent=['notebooks'])


def test_notebooks_no():
    check_project(
        settings={'use_notebooks': 'no'},
        files_non_existent=['notebooks'])


def test_docker_yes():
    check_project(
        settings={'use_docker': 'yes'},
        files_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])


def test_docker_no():
    check_project(
        settings={'use_docker': 'no'},
        files_non_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])


def test_config_hocon():
    check_project(
        settings={'config_file': 'hocon'},
        files_existent=['src/{module_name}/util.py', 'src/{module_name}/res/default.conf',
                        'config/debug.conf'],
        files_non_existent=['config/config.yml'],
        test_cli=True, run_pytest=True)


def test_config_yaml():
    check_project(
        settings={'config_file': 'yaml'},
        files_existent=['src/{module_name}/util.py', 'config/config.yml'],
        files_non_existent=['config/debug.conf', 'src/{module_name}/res/default.conf'],
        test_cli=True, run_pytest=True)


def test_config_none():
    check_project(
        settings={'config_file': 'none'},
        files_non_existent=['config', 'src/{module_name}/util.py', 'tests/util.py',
                            'src/{module_name}/res'],
        test_cli=True)


@pytest.mark.skip(reason="not yet implemented")
def test_formatter_black():
    # TODO implement
    check_project(
        settings={'code_formatter': 'black'})


@pytest.mark.skip(reason="nothing to test until black is implemented")
def test_formatter_none():
    # TODO implement
    check_project(
        settings={'code_formatter': 'none'})


def test_editor_pycharm():
    check_project(
        settings={'editor_settings': 'pycharm'},
        files_existent=['.idea'],
        files_non_existent=['.vscode'])


def test_editor_vscode():
    check_project(
        settings={'editor_settings': 'vscode'},
        files_existent=['.vscode/settings.json'],
        files_non_existent=['.idea'])


def test_editor_none():
    check_project(
        settings={'editor_settings': 'none'},
        files_non_existent=['.idea', '.vscode'])
