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


def test_docker():
    check_project(
        settings={'use_docker': 'yes'},
        files_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])


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
