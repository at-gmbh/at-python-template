from pathlib import Path

from .util import assert_file_contains, check_project


def test_base():
    check_project(run_pytest=True)


def test_pip():
    check_project(
        settings={'package_manager': 'pip'},
        files_existent=['requirements.txt', 'requirements-dev.txt', 'setup.py'],
        files_non_existent=['environment.yml', 'environment-dev.yml'])


def test_conda():
    check_project(
        settings={'package_manager': 'conda'},
        files_existent=['environment.yml', 'environment-dev.yml', 'setup.py'])


def test_poetry():
    check_project(
        settings={'package_manager': 'poetry'},
        files_existent=['pyproject.toml'],
        files_non_existent=['environment.yml, environment-dev.yml', 'requirements.txt', 'requirements-dev.txt', 'setup.py']
    )


def test_notebooks_yes():
    check_project(
        settings={'use_notebooks': 'yes'},
        files_existent=['notebooks'])


def test_notebooks_no():
    check_project(
        settings={'use_notebooks': 'no'},
        files_non_existent=['notebooks'])


def test_docker_pip():
    check_project(
        settings={'use_docker': 'yes', 'package_manager': 'pip',},
        files_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])


def test_docker_conda():
    check_project(
        settings={'use_docker': 'yes', 'package_manager': 'conda',},
        files_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])


def test_docker_poetry():
    check_project(
        settings={'use_docker': 'yes', 'package_manager': 'poetry',},
        files_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore']
    )


def test_docker_no():
    check_project(
        settings={'use_docker': 'no'},
        files_non_existent=['Dockerfile', 'docker-compose.yml', '.dockerignore'])


def test_cli_yes():
    check_project(
        settings={'create_cli': 'yes'},
        files_existent=['src/{module_name}/main.py', 'src/{module_name}/__main__.py'],
        test_cli=True)


def test_cli_no():
    check_project(
        settings={'create_cli': 'no'},
        files_non_existent=['src/{module_name}/__main__.py'],
        test_cli=False)


def test_config_hocon():
    check_project(
        settings={'config_file': 'hocon', 'create_cli': 'yes'},
        files_existent=['src/{module_name}/util.py', 'src/{module_name}/res/default.conf',
                        'config/debug.conf'],
        files_non_existent=['config/config.yml'],
        test_cli=True, run_pytest=True)


def test_config_yaml():
    check_project(
        settings={'config_file': 'yaml'},
        files_existent=['src/{module_name}/util.py', 'config/config.yml'],
        files_non_existent=['config/debug.conf', 'src/{module_name}/res/default.conf'],
        run_pytest=True)


def test_config_none():
    check_project(
        settings={'config_file': 'none'},
        files_non_existent=['config', 'src/{module_name}/util.py', 'tests/util.py',
                            'src/{module_name}/res'])


def test_formatter_black_pip():
    def check_black(project_dir: Path):
        assert_file_contains(project_dir / '.pre-commit-config.yaml', contains='psf/black')
        assert_file_contains(project_dir / 'requirements-dev.txt', contains='black')

    check_project(
        settings={'code_formatter': 'black', 'package_manager': 'pip'},
        fun=check_black)


def test_formatter_black_conda():
    def check_black(project_dir: Path):
        assert_file_contains(project_dir / '.pre-commit-config.yaml', contains='psf/black')
        assert_file_contains(project_dir / 'environment-dev.yml', contains='black=')

    check_project(
        settings={'code_formatter': 'black', 'package_manager': 'conda'},
        fun=check_black)


def test_formatter_black_poetry():
    def check_black(project_dir: Path):
        assert_file_contains(project_dir / '.pre-commit-config.yaml', contains='psf/black')
        assert_file_contains(project_dir / 'pyproject.toml', contains='black')

    check_project(
        settings={'code_formatter': 'black', 'package_manager': 'poetry'},
        fun=check_black
    )


def test_formatter_none():
    def check_white(project_dir: Path):
        assert_file_contains(project_dir / '.pre-commit-config.yaml', not_contains='psf/black')
        assert_file_contains(project_dir / 'environment-dev.yml', not_contains='black=')

    check_project(
        settings={'code_formatter': 'none'},
        fun=check_white)


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


def test_random_combination():
    check_project(
        settings={
            'package_manager': 'pip',
            'use_notebooks': 'no',
            'config_file': 'hocon',
            'use_docker': 'yes',
            'create_cli': 'yes',
            'code_formatter': 'none',
            'editor_settings': 'pycharm',
        },
        test_cli=True, run_pytest=True)


def test_poetry_regression():
    """
    Regression test for the bug:
    Template test failure after creating template with package_manager=poetry
    """
    check_project(
        settings={
            "package_manager": "poetry",
            "use_notebooks": "no",
            "config_file": "none",
            "use_docker": "no",
            "create_cli": "no",
            "code_formatter": "none",
            "editor_settings": "none",
        },
        test_cli=False,
        run_pytest=True,
    )
