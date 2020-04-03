# Python Project Template

A cookiecutter template designed to bridge the gap between exploratory work and production-ready projects. The goal is to be able to quickly bootstrap a Python project that provides lots of useful stuff to build, test & deploy your code without being overly convoluted like many of the publicly available packages.

## Getting Started

1. [`pip install -U cookiecutter`](https://pypi.org/project/cookiecutter/)
2. `cookiecutter https://bitbucket.alexanderthamm.com/scm/at-commons/python-project-template.git` (HTTPS) or
   `cookiecutter ssh://git@bitbucket.alexanderthamm.com:7999/at-commons/python-project-template.git` (SSH)
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

* [Python templates on Github](https://github.com/cookiecutter/cookiecutter#python): a curated list of Python templates in cookiecutter's readme.

## Contact

* Sebastian Straub (sebastian.straub@alexanderthamm.com)
* Steffen Bunzel (steffen.bunzel@alexanderthamm.com)
* Hans Rauer (hans.rauer@alexanderthamm.com)
* Simon Weiß (simon.weiss@alexanderthamm.com)
* Jan Bilek (jan.bilek@alexanderthamm.com)