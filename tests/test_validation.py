import pytest
from cookiecutter.exceptions import CookiecutterException

from .util import check_project


def test_module_name():
    with pytest.raises(CookiecutterException):
        check_project(settings={'module_name': "don't you tell *me* how to name *my* modules!"})


def test_project_slug():
    with pytest.raises(CookiecutterException):
        check_project(settings={'project_slug': "I am afraid of snails"})


def test_editor():
    check_project(settings={'editor_settings': "hax0r-editor-2000"})
    # note: invalid choices will be silently ignored by cookiecutter
