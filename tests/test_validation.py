from runpy import run_path
from typing import Any, Callable

import pytest
from cookiecutter.exceptions import CookiecutterException
from pytest_mock import MockerFixture

from .util import check_project


def test_module_name():
    with pytest.raises(CookiecutterException):
        check_project(settings={'module_name': "don't you tell *me* how to name *my* modules!"})


def test_project_slug():
    with pytest.raises(CookiecutterException):
        check_project(settings={'project_slug': "I am afraid of snails"})


def test_editor():
    check_project(settings={'editor_settings': "pycharm"})


def test_fail_python_3_8(mocker: MockerFixture):
    fail_python_version(mocker, "3.8.0")


def test_fail_python_2_7(mocker: MockerFixture):
    fail_python_version(mocker, "2.7.0")


def test_fail_cookiecutter_1_6_0(mocker: MockerFixture):
    fail_cookiecutter_version(mocker, "1.6.0")


def test_fail_cookiecutter_1_7_1(mocker: MockerFixture):
    fail_cookiecutter_version(mocker, "1.7.1")


def fail_python_version(mocker: MockerFixture, version_info: str):
    patch_cookiecutter_run_script(
        mocker, lambda mocker: mocker.patch('platform.python_version', lambda: version_info))
    with pytest.raises(SystemExit):
        check_project()


def fail_cookiecutter_version(mocker: MockerFixture, version_info: str):
    patch_cookiecutter_run_script(
        mocker, lambda mocker: mocker.patch('cookiecutter.__version__', version_info))
    with pytest.raises(SystemExit):
        check_project()


def patch_cookiecutter_run_script(mocker: MockerFixture, patch_fun: Callable[[MockerFixture], Any]):
    def run_script_wrapper(script_path, *args, **kwargs):
        patch_fun(mocker)
        run_path(script_path)
    mocker.patch('cookiecutter.hooks.run_script', run_script_wrapper)
