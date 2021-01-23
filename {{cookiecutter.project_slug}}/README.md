# {{ cookiecutter.project_name }}
{{ cookiecutter.project_short_description }}
{% set py_command = 'poetry run python' if cookiecutter.package_manager == 'poetry' else 'python' -%}
{% set test_command = 'poetry run pytest tests' if cookiecutter.package_manager == 'poetry' else 'python setup.py test' -%}
{% set test_cov_command = 'poetry run pytest tests --cov=src --cov-report=xml' if cookiecutter.package_manager == 'poetry' else 'python setup.py testcov' -%}
{% set build_command = 'poetry build' if cookiecutter.package_manager == 'poetry' else 'python setup.py dist' %}
{% set install_command = 'poetry add' if cookiecutter.package_manager == 'poetry' else 'conda install' if cookiecutter.package_manager == 'conda' else 'pip install' %}
## Getting Started
{% if cookiecutter.package_manager == 'conda' %}
To set up your local development environment, please use a fresh virtual environment.

To create the environment run:

    conda env create --name {{ cookiecutter.project_slug }} --file=environment-dev.yml

To activate the environment run:

    conda activate {{ cookiecutter.project_slug }}

To update this environment with your production dependencies run:

    conda env update --file=environment.yml
{% elif cookiecutter.package_manager == 'pip' %}
To set up your local development environment, please use a fresh virtual environment.

Then run:

    pip install -r requirements.txt -r requirements-dev.txt
{% else %}
To set up your local development environment, run:

    poetry install

Behind the scenes, this creates a virtual environment and installs {{ cookiecutter.module_name }} along with its dependencies (like `pip install -e .`) into that virtualenv. Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.
{% endif -%}

{% if cookiecutter.create_cli == 'yes' %}
You can now run the module from the `src` directory with `{{ py_command }} -m {{ cookiecutter.module_name }}`.
{% else %}
You can now import functions and classes from the module with `import {{ cookiecutter.module_name }}`.
{% endif -%}

{% if cookiecutter.use_docker == 'yes' %}
If you want to deploy this project as a docker container, please ensure that [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed, then run

    docker-compose up

this will build the entire project with all dependencies inside a docker container. You may use the command line interface of the application now, e.g. by editing the `command` tag in the [`docker-compose.yml`](./docker-compose.yml).
{% endif %}
### Testing

We use `pytest` as test framework. To execute the tests, please run

    {{ test_command }}

To run the tests with coverage information, please use

    {{ test_cov_command }}

and have a look at the `htmlcov` folder, after the tests are done.
{% if cookiecutter.use_notebooks == 'yes' %}
### Notebooks
{% if cookiecutter.package_manager == 'poetry' %}
You can use your module code (`src/`) in Jupyter notebooks (`notebooks/`) without running into import errors by running:

    poetry run jupyter notebook

or

    poetry run jupyter-lab

This starts the jupyter server inside the project's virtualenv.
{% else %}
To use your module code (`src/`) in Jupyter notebooks (`notebooks/`) without running into import errors, make sure to install the source locally

    pip install -e .

This way, you'll always use the latest version of your module code in your notebooks via `import {{ cookiecutter.module_name }}`.
{% endif %}

Assuming you already have Jupyter installed, you can make your virtual environment available as a separate kernel by running:

    {{ install_command }} ipykernel
    {{ py_command }} -m ipykernel install --user --name="{{ cookiecutter.project_name }}"

Note that we mainly use notebooks for experiments, visualizations and reports. Every piece of functionality that is meant to be reused should go into module code
and be imported into notebooks.
{% endif %}
### Distribution Package

To build a distribution package (wheel), please use

    {{ build_command }}

this will clean up the build folder and then run the `bdist_wheel` command.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit && pre-commit install

## Contact

{{ cookiecutter.full_name }} ({{ cookiecutter.email }})

## License

{% if cookiecutter.company_name %}© {{cookiecutter.company_name}}{% else %}© {{cookiecutter.full_name}}{% endif %}
