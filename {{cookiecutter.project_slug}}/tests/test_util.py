from {{ cookiecutter.module_name }} import util


def test_get_resource_string():
    s = util.get_resource_string('version.py')
    assert '__version__ = ' in s
