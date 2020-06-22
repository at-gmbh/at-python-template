import logging

import typer

from {{ cookiecutter.module_name }} import __title__
from {{ cookiecutter.module_name }} import __version__{% if cookiecutter.config_file != 'none' %}
from {{ cookiecutter.module_name }} import util{% endif %}

logger = logging.getLogger('{{ cookiecutter.module_name }}')


app = typer.Typer(
    name='{{ cookiecutter.module_name }}',
    help="{{ cookiecutter.project_short_description }}")


def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__} {__version__}")
        raise typer.Exit()


ConfigOption = typer.Option(
    {% if cookiecutter.config_file == 'yaml' %}...{% else %}None{% endif %}, '-c', '--config', metavar='PATH', help="path to the program configuration")
VersionOption = typer.Option(
    None, '-v', '--version', callback=version_callback, is_eager=True,
    help="print the program version and exit")


@app.command()
def main(config_file: str = ConfigOption, version: bool = VersionOption):
    """
    This is the entry point of your command line application. The values of the CLI params that
    are passed to this application will show up als parameters to this function.

    This docstring is where you describe what your command line application does.
    Try running `python -m {{ cookiecutter.module_name }} --help` to see how this shows up in the command line.
    """
    {% if cookiecutter.config_file != 'none' %}config = util.load_config(config_file)
    util.logging_setup(config){% endif %}
    logger.info("Looks like you're all set up. Let's get going!")
    # TODO your journey starts here


if __name__ == "__main__":
    app()
