import typer

from {{ cookiecutter.module_name }}.cli import main
typer.run(main)
