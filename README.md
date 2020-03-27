# Python Factory Template

A cookiecutter template designed for production-ready projects, especially, but not limited to, projects in the AT Data Factory. The goal is to be able to quickly bootstrap a Python project with a clear target in sight, therefore no experimentation with Jupyter Notebooks, but lots of useful stuff to build, test & deploy your code.

## Getting Started

1. [`pip install -U cookiecutter`](https://pypi.org/project/cookiecutter/)
2. `cookiecutter https://bitbucket.alexanderthamm.com/scm/atu/python-app-template.git` (HTTPS) or  
   `cookiecutter ssh://git@bitbucket.alexanderthamm.com:7999/atu/python-app-template.git` (SSH)
3. profit!

Feedback and contributions are welcome!

## Features

* `README.md`: arguably *the* most important file of your project. Write it so that someone who knows nothing about your project can build the code, run the tests and start working on the code after reading this document.
* project structure
  - `{my_package}`
  - `tests`
* setup
  - `setup.py`
  - `requirements.txt`
  - `requirements-dev.txt`: Dependencies for developers. Please install to make full use of many useful features (e.g. tests, pre-commit hooks, etc.)
* ignore
  - `.gitignore`
  - `.dockerirgnore`
* Docker
  - `Dockerfile`
  - `docker-compose.yml`
* code conventions
  - [`.editorconfig`](https://editorconfig.org/): ensures that all your text files use the same style, e.g. tabs vs. spaces, indent size, trailing whitespace, and so on. Supported by [many popular editors](https://editorconfig.org/#download), but not everywhere.
  - `.pre-commit-config.yaml`: notifies you of common issues when you make a commit, like committing a huge binary file. Relies on the [`pre-commit`](https://pre-commit.com/) package.

## Other Templates

* [atutils/python-app-template](https://bitbucket.alexanderthamm.com/projects/ATU/repos/python-app-template/browse): support for Jupyter Notebooks, focus on data exploration.
* [Python templates on Github](https://github.com/cookiecutter/cookiecutter#python): a curated list of Python templates in cookiecutter's readme. 

## Contact

Sebastian Straub (sebastian.straub@alexanderthamm.com)
