# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Getting Started

To set up your local development environment, please use a fresh virtualenv, then run
{% if cookiecutter.package_manager == 'conda' %}
    conda env create -n {{ cookiecutter.project_slug }} -f environment-dev.yml

To activate this environment run:

    conda activate {{ cookiecutter.project_slug }}
{% else %}
    pip install -r requirements.txt
{% endif %}
You can now run the module from the `src` directory with `python -m {{ cookiecutter.module_name }}`.

If you want to deploy this project as a docker container, please ensure that [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed, then run

    docker-compose up

this will build the entire project with all dependencies inside a docker container. You may use the command line interface of the application now, e.g. by editing the `command` tag in the [`docker-compose.yml`](./docker-compose.yml).

### Testing

We use `pytest` as test framework. To execute the tests, please run

    python setup.py test

To run the tests with coverage information, please use

    python setup.py testcov

and have a look at the `htmlcov` folder, after the tests are done.

### Distribution Package

To build a distribution package (wheel), please use

    python setup.py dist

this will clean up the build folder and then run the `bdist_wheel` command.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit && pre-commit install

## License

© Alexander Thamm GmbH
