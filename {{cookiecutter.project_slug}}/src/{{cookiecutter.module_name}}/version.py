{% if cookiecutter.package_manager == 'poetry' %}from importlib.metadata import version

__version__ = version("{{ cookiecutter.project_slug }}")
{%- else %}__version__ = '0.1.0'{% endif %}
