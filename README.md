# AT Python Template

This is the official Python Project Template of Alexander Thamm GmbH (AT). It is built with [cookiecutter](https://cookiecutter.readthedocs.io/) and was designed to bridge the gap between exploratory work and production-ready projects. The goal is to be able to quickly bootstrap a Python project that provides lots of useful stuff to build, test & deploy your code without being overly convoluted like many of the publicly available packages.

## Getting Started

1. [`conda install -c conda-forge cookiecutter`](https://anaconda.org/conda-forge/cookiecutter) or [`pip install -U cookiecutter`](https://pypi.org/project/cookiecutter/)

> This template requires `cookiecutter>=1.7.2`.
  If you experience issues installing it into your default
  (virtual) environment in (`pip`) `conda`, we recommend to create a 
  new clean environment with nothing but the `cookiecutter` package
  installed.

2. `cookiecutter https://github.com/at-gmbh/at-python-template`
3. profit!


![image](setup_prompt.gif "Setup a professional python project in seconds")

This will install or update cookiecutter on your system and create a new project in the current folder using the AT Python Template. Please note: Python 3.6 or higher is required.

Feedback and contributions are very welcome! Learn more in the [Contributing](#contributing) section below.

## Choices Explained

Unfortunately, cookiecutter does not allow us to show any description of the options in the setup dialogue (though this will change when [cookiecutter 2.0](https://github.com/cookiecutter/cookiecutter/projects/3) is released), so here's some more info on that:

* `full_name [Jane Doe]`: enter your name here. It will be used in the Readme and the setup script.
* `company_name []`: enter your company's name here. The default is to leave this blank.
* `email [contact@alexanderthamm.com]`: your email address, also for *Readme.md* and *setup.py*.
* `project_name [My Project]`: the name of your project. This is the "pretty" version of your project name, it may contain whitespace and all of your favorite emojis.
* `project_slug [my-project]`: this is the project slug. It is automatically derived from your project name, uses dashes instead of whitespace and must not contain any special characters. This will also be the name of your Python package.
* `module_name [my_project]`: this is the name of your Python module. It is similar to the project slug, but uses underscores instead of dashes. This is because for Python module names, the same restrictions apply as for Python variable names and `-` cannot be used in a variable name.
* `project_short_description [a short summary of the project]`: please write a short summary (ideally one sentence) of your project here. It will be used in the Readme and the setup script.
* Select your `package_manager`
  - `conda` (default): use [conda](https://docs.conda.io/) as your package manager and `environment.yml` to track your dependencies. Conda allows you to easily manage virtual environments and Python versions and there are hardly any issues with installing packages on Windows. Therefore we recommend this option for most users.
  - `pip`: use [pip](https://pip.pypa.io/) as your package manager and `requirements.txt` to track your dependencies. Unlinke conda, pip is only a package manager: it does not manage your Python environment and there might be some issues with package installation on Windows if no pre-compiled binaries are available. However, pip is lightweight, comes with every Python distribution and is the default in the Python community. Recommended for power users or projects that will be used in production environments or when Docker is your target (most Python-based Docker images don't include conda).
* `use_notebooks` (yes or no): if you want to use Jupyter Notebooks, we'll set you up so that all your notebooks will be stored in the `notebooks` folder and you can easily call functions that are defined in your Python package from the notebooks. This should ease the transition from exploration (using notebooks) to production (using code specified in the module) and allow early sharing of code.
* `use_docker` (yes or no): if you plan to build a Docker image, select *yes* and we'll set you up with a Dockerfile and other docker-related stuff.
* `create_cli` (yes or no): if you plan to build an application with a command line interface (CLI), select *yes* here. This will integrate a template for the CLI into your project - minimal boilerplate guaranteed! (We're leveraging the awesome [typer](https://typer.tiangolo.com/) library for this.)
* `config_file`: select your preferred config format. It is best practice to store your configuration separate from your code, even for small projects, but because there are a gazillion ways to do this, each project seems to reinvents the wheel. We want to provide a few options to set you up with a working configuration:
  - `yaml`: use [YAML](https://yaml.org/) as your configuration file format. Easy to read and write, widely adopted, relies on the [PyYAML](https://pyyaml.org/) package.
  - `hocon`: use [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) as your configuration file format. It is a superset of JSON, very resilient (it's really hard to make a breaking syntax error) and comes with powerful functions, e.g. for inheritance or variable substitution. Relies on the [pyhocon](https://github.com/chimpler/pyhocon/) package.
  - `none`: don't need any configuration or want to do your own thing? choose this option.
* `code_formatter`: a code formatter is a powerful tool that can help teams to stick to a common code style. However, a formatter cannot solve every code style problem for you and it may lead to issues for users that are not aware of how it works. Always talk to your team about [PEP 8](https://www.python.org/dev/peps/pep-0008/) and a common code style, then choose the right formatter for you (or none at all):
  - [`black`](https://github.com/psf/black): *the uncompromising Python code formatter*. 
  - `none`: don't use a code formatter.
* `editor_settings`: there are many editors out there with great support for Python projects. However, because Python gives you a lot of freedom in terms of structuring your project or the tools you use, configuring your editor for each project can be intricate and repetitive. If your favourite editor is in the list, we'll get you started with a working config for your project. Please note that this config will not be checked into the git repo (that would be bad practice; every developer should be free to use whatever editor they like) and therefore this config will only be available to you.
  - `vscode`: add config for [Visual Studio Code](https://code.visualstudio.com/)
  - `pycharm`: add config for [PyCharm](https://www.jetbrains.com/pycharm/)
  - `none`: no editor config / set it up by yourself

## Features

* `README.md`: arguably *the* most important file of your project. It's the first thing anyone will see who looks at your project. Write it so that someone who doesn't know anything about your project can build the code, run tests and start working on the code after reading this document. Check out [makeareadme.com](https://www.makeareadme.com/) to learn about best practices and have a look at [awesome-readme](https://github.com/matiassingers/awesome-readme) for examples of awesome readme files.
* Code structure
  - `src/{my_module}`: this is your module - all your Python code should be stored here. Make sure to add the `src` folder to your `PYTHONPATH` or tell your IDE that this is where your sources are, if it didn't figure that out by itself. While you could have your module folder at the root of your git repo, there are [some good reasons](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure) why using a `src` folder may be the better solution.
  - `tests`: tests are defined under this folder. We use [pytest](https://docs.pytest.org/) as our test framework by default.
  - `notebooks`: drop your Jupyter notebooks in this folder and remember to move frequently used code to the module folder as soon as possible, or you'll end up with a bunch of spaghetti code spread out over way too many notebooks.
  - `config`: store your config files in this folder. Don't hesitate to create variants of your config files for different environments (e.g. debugging, integration, production)
* setup
  - `setup.py`: this is the standard Python [Setup Script](https://setuptools.readthedocs.io/en/latest/setuptools.html). It allows you to install your module, create distribution packages and much more.
  - conda:
    * `environment.yml`: definition of an environment that can run the module. Does not include tests or developer tools. 
    * `environment-dev.yml`: definition of an environment for developers. Please install to make full use of many useful features (e.g. tests, pre-commit hooks, etc.)
  - pip:
    * `requirements.txt`: dependencies that are required to run the module. Does not include tests or developer tools. 
    * `requirements-dev.txt`: dependencies for developers. Please install to make full use of many useful features (e.g. tests, pre-commit hooks, etc.)
* Docker
  - `Dockerfile`
  - `docker-compose.yml`
  - `.dockerignore`
* those files starting with a dot
  - `.gitignore`
  - [`.editorconfig`](https://editorconfig.org/): ensures that all your text files use the same style, e.g. tabs vs. spaces, indent size, trailing whitespace, and so on. Supported by [many popular editors](https://editorconfig.org/#download), but not everywhere.
  - `.pre-commit-config.yaml`: notifies you of common issues when you make a commit, like committing a huge binary file. Relies on the [`pre-commit`](https://pre-commit.com/) package.
  - settings for specific editors
    * `.vscode`: Settings for VSCode. Sets *pytest* as default test framework and configures automatic code formatting if requested, among other things.
    * `.idea`: Settings for PyCharm. Marks `./src` as source folder, sets *pytest* as default test framework and *reStructuredText* as default docstring format.

## Contributing

Contributions to this project are very welcome. Please open a ticket on the [issues page](https://github.com/at-gmbh/at-python-template/issues) if you have found any bugs or if you have ideas for improvements. If you want to contribute code, we'd love to review your [pull request](https://github.com/at-gmbh/at-python-template/pulls)!

This Readme file contains our technical documentation, a user guide can be found in [Confluence](https://confluence.alexanderthamm.com/display/ATTECH/Python+Project+Template%3A+AT+Cookiecutter) and our Teams channel is [AT Commons - Python App Template](https://teams.microsoft.com/l/channel/19%3a5c4a54a84e144283818450bb6316fa58%40thread.tacv2/Python%2520App%2520Template?groupId=5907ba79-097d-4906-8c58-fdbfa98fe901&tenantId=44d8cd30-12b4-46ab-82b4-56bec7d7a555). Please don't hesitate to contact one of the persons listed at the end of this document to get started. Confluence and Teams can only be accessed by AT employees; however, you're very welcome to discuss issues, submit PRs and contact the developers by mail (see below) if you're not an AT employee.

Hints for developers:

* install dependencies in a fresh virtualenv with `pip install -r requirements.txt`
* run unit tests with `pytest tests`. There are unit tests for every available choice in [`tests/test_options.py`](./tests/test_options.py). If you add more choices, please update these tests.
* be careful with code formatters: Many files in this project contain [jinja2 templates](https://jinja.palletsprojects.com) (you'll find statements like `{% if cookiecutter.config_file == 'yaml' %}...{% endif %}` all over the place). These templates mean that the source code becomes syntactically incorrect and some formatters might do unexpected things.

## Other Templates

You may find lots of other templates under the [cookiecutter-template](https://github.com/topics/cookiecutter-template) tag on GitHub. Some of the most popular templates (by Github Stars) can be found on [awesomeopensource.com](https://awesomeopensource.com/projects/cookiecutter).

## Contact

* Sebastian Straub (sebastian.straub [at] alexanderthamm.com)
* Steffen Bunzel (steffen.bunzel [at] alexanderthamm.com)
* Hans Rauer (hans.rauer [at] alexanderthamm.com)
* Simon Weiß (simon.weiss [at] alexanderthamm.com)
* Honza Bílek (jan.bilek [at] alexanderthamm.com)

## License

    Copyright 2020 Alexander Thamm GmbH
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
