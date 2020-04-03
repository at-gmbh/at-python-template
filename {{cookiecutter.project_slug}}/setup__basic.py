from pathlib import Path
from runpy import run_path

from setuptools import find_packages, setup

# read the program version from version.py (without loading the module)
__version__ = run_path('{{ cookiecutter.project_slug }}/version.py')['__version__']

setup(
    name="{{ cookiecutter.project_name }}",
    version=__version__,
    author="{{ cookiecutter.full_name }}",
    author_email="{{ cookiecutter.email }}",
    description="{{ cookiecutter.project_short_description }}",
    license="proprietary",
    url="",
    packages=find_packages(exclude=['tests*']),
    long_description=(Path(__file__).parent / 'README.md').open().read(),
    install_requires=[],
    tests_require=[
        'pytest',
    ],
    platforms='any',
    python_requires='>=3.7',
)
