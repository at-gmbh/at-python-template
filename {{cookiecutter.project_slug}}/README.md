{#- ------------------------------------------ -#}
{#-      Definition of Template Variables      -#}
{#- ------------------------------------------ -#}
{%- set py_command = 'poetry run python' if cookiecutter.package_manager == 'poetry' else 'python' -%}
{%- set test_command = 'poetry run pytest tests' if cookiecutter.package_manager == 'poetry' else 'python setup.py test' -%}
{%- set test_cov_command = 'poetry run pytest tests --cov=src --cov-report=xml' if cookiecutter.package_manager == 'poetry' else 'python setup.py testcov' -%}
{%- set build_command = 'poetry build' if cookiecutter.package_manager == 'poetry' else 'python setup.py dist' -%}
{%- set install_command = 'poetry add' if cookiecutter.package_manager == 'poetry' else 'conda install' if cookiecutter.package_manager == 'conda' else 'pip install' -%}
{#- ------------------------------------------ -#}
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Getting Started
{% if cookiecutter.package_manager == 'conda' %}
To set up your local development environment, please use a fresh virtual environment with:

    conda env create --name {{ cookiecutter.project_slug }} --file=environment-dev.yml

Then activate the environment with:

    conda activate {{ cookiecutter.project_slug }}

To update this environment with your production dependencies, please run:

    conda env update --file=environment.yml
{% elif cookiecutter.package_manager == 'pip' %}
To set up your local development environment, please use a fresh virtual environment (`python -m venv .venv`), then run:

    pip install -r requirements.txt -r requirements-dev.txt
    pip install -e .

The first command will install all requirements for the application and to execute tests.
With the second command, you'll get an editable installation of the module, so that imports work properly.
{% elif cookiecutter.package_manager == 'poetry' %}
To set up your local development environment, please run:

    poetry install

Behind the scenes, this creates a virtual environment and installs `{{ cookiecutter.module_name }}` along with its dependencies into a new virtualenv.
Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.

{% elif cookiecutter.package_manager == 'uv' %}
## Using `uv` for Project Setup

> 🧰 **Note:** You do **not** need to have Python pre-installed.  
> `uv` includes its own Python runtime and manages everything automatically.

### 🔧 Installing `uv`

Install `uv` using the official script:

> For macOS and Linux (bash):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> For Windows (PowerShell):

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

For more install options, see: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

---

### 🚀 Getting Started

1. **Install all dependencies defined in `pyproject.toml`:**

    ```bash
    uv sync
    ```

2. **(Optional) Add new dependencies during development:**

    ```bash
    uv add <package-name>
    ```

    Example:

    ```bash
    uv add requests
    ```

3. **Run Python or project scripts:**

    Recommended:

    ```bash
    uv run python
    ```

    Or, if using scripts defined in `pyproject.toml`:

    ```bash
    uv run <your-script>
    ```

---

### ⚙️ Alternative: Manual virtual environment activation

If you prefer using `python` directly, activate the `uv`-managed virtual environment:

- macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```

- Windows (CMD):

    ```cmd
    .venv\Scripts\activate
    ```

- Windows (PowerShell):

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

Then run:

```bash
python your_script.py
```

To deactivate:

```bash
deactivate
```
{% endif -%}

{% if cookiecutter.create_cli == 'yes' %}
You can now access the CLI with `{{ py_command }} -m {{ cookiecutter.module_name }}`.
{% else %}
You can now import functions and classes from the module with `import {{ cookiecutter.module_name }}`.
{% endif -%}

{% if cookiecutter.use_docker == 'yes' %}
If you want to deploy this project as a docker container, please ensure that [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed, then run

    docker-compose up

this will build the entire project with all dependencies inside a docker container. You may use the command line interface of the application now, e.g. by editing the `command` tag in the [`docker-compose.yml`](./docker-compose.yml).
{% endif %}
### Testing

We use `pytest` as the test framework. To run tests, use:

{% if cookiecutter.package_manager == 'poetry' %}
    poetry run pytest tests
{% elif cookiecutter.package_manager == 'uv' %}
    uv run pytest tests
{% else %}
    pytest tests
{% endif %}

To run tests with coverage reporting:

{% if cookiecutter.package_manager == 'poetry' %}
    poetry run pytest tests --cov=src --cov-report=html --cov-report=term
{% elif cookiecutter.package_manager == 'uv' %}
    uv run pytest tests --cov=src --cov-report=html --cov-report=term
{% else %}
    pytest tests --cov=src --cov-report=html --cov-report=term
{% endif %}

After running the tests, open the `htmlcov` directory in your browser to inspect coverage visually.

{% if cookiecutter.use_notebooks == 'yes' %}
### Notebooks

You can use your module code (`src/`) in Jupyter notebooks (`notebooks/`) without running into import errors.

{% if cookiecutter.package_manager == 'poetry' %}
Launch the Jupyter server from the project's virtualenv:

    poetry run jupyter notebook

or

    poetry run jupyter-lab

{% elif cookiecutter.package_manager == 'uv' %}
Launch Jupyter notebooks within the `uv` environment:

    uv run jupyter notebook

or

    uv run jupyter-lab

{% elif cookiecutter.package_manager == 'conda' %}
Make sure your conda environment is activated, then launch:

    jupyter notebook

or

    jupyter lab

{% else %}
First, make sure to install your package in editable mode:

    pip install -e .

Then launch Jupyter:

    jupyter notebook

or

    jupyter lab
{% endif %}

To make your virtual environment available as a Jupyter kernel, run:

    {{ install_command }} ipykernel
    {{ py_command }} -m ipykernel install --user --name="{{ cookiecutter.project_slug }}"

> 💡 This ensures that your notebook environment uses the same dependencies and paths as your project.

Note: We mainly use notebooks for experimentation, visualizations, and reporting. Any reusable logic should live in the `src/` module and be imported into notebooks.
{% endif %}
### Distribution Package

To build a distribution package (wheel), run:

{% if cookiecutter.package_manager == 'poetry' %}
    poetry build
{% elif cookiecutter.package_manager == 'uv' %}
    uv run python -m build
{% elif cookiecutter.package_manager == 'conda' %}
    python setup.py sdist bdist_wheel
{% else %}
    python setup.py bdist_wheel
{% endif %}

{% if cookiecutter.package_manager == 'uv' %}
> 💡 If `build` is not yet added to your project, install it with:

    uv add --dev build
{% elif cookiecutter.package_manager == 'poetry' %}
> 💡 `poetry build` handles everything including packaging, metadata, and versioning.
{% elif cookiecutter.package_manager == 'pip' %}
> 💡 Make sure `wheel` and `build` are installed:

    pip install build wheel
{% elif cookiecutter.package_manager == 'conda' %}
> 💡 If needed, install wheel via:

    conda install wheel
{% endif %}

Build artifacts will be placed in the `dist/` directory.


### Contributions

Before contributing, please set up the pre-commit hooks to ensure consistent formatting and linting.

{% if cookiecutter.package_manager == 'poetry' %}
Install the hooks with:

    poetry run pre-commit install
{% elif cookiecutter.package_manager == 'uv' %}
Install the hooks with:

    uv run pre-commit install
{% else %}
    pip install -U pre-commit
    pre-commit install
{% endif %}

> This will automatically run checks like code formatting, import sorting, and linting before each commit.

To uninstall the hooks:

{% if cookiecutter.package_manager == 'poetry' %}
    poetry run pre-commit uninstall
{% elif cookiecutter.package_manager == 'uv' %}
    uv run pre-commit uninstall
{% else %}
    pre-commit uninstall
{% endif %}

## Contact

{{ cookiecutter.full_name }} ({{ cookiecutter.email }})

## License

{% if cookiecutter.company_name %}© {{cookiecutter.company_name}}{% else %}© {{cookiecutter.full_name}}{% endif %}
