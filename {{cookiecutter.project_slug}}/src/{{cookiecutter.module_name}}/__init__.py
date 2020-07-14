"""
{{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}
"""

__title__ = "{{ cookiecutter.project_slug }}"
{% if cookiecutter.company_name %}
__copyright__ = "© {% now 'utc', '%Y' %} {{ cookiecutter.company_name }}"
{% else %}
__copyright__ = "© {% now 'utc', '%Y' %} {{ cookiecutter.full_name }}"
{% endif %}
from .version import __version__
