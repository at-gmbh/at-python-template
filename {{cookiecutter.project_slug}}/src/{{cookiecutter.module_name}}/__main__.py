{% if cookiecutter.create_cli == 'yes' %}from {{ cookiecutter.module_name }}.main import app
app(){% else %}from {{ cookiecutter.module_name }}.main import main
main(){% endif %}
