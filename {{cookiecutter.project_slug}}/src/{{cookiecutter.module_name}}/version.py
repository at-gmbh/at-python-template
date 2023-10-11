{% if cookiecutter.package_manager == 'poetry' %}try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("{{ cookiecutter.project_slug }}")
{%- else %}__version__ = '0.1.0'{% endif %}
