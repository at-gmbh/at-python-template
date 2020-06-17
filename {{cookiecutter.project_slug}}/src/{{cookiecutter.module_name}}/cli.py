"""
The command line interface for {{ cookiecutter.module_name }}.

If you're calling this module from Python instead of using the cli, please use the
``cli.main()`` function and pass your arguments as standard function arguments.
"""
import typer
import sys

from {{ cookiecutter.module_name }} import __version__{% if cookiecutter.config_file != 'none' %}
from {{ cookiecutter.module_name }} import util{% endif %}


def version_callback(value: bool):
    if value:
        typer.echo("my-project " + __version__)
        raise typer.Exit()


def main(
    {% if cookiecutter.config_file != 'none' %}config: str = typer.Option(None, help="Path to the program configuration"),{% endif %}
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """
    This is where you describe what your command line application does.
    Try running `python -m {{ cookiecutter.module_name }} --help` how this shows up in the command line.

    See the typer docs for more details: https://typer.tiangolo.com/
    """

    {% if cookiecutter.config_file != 'none' %}if config:
        config = util.load_config(config)
        util.logging_setup(config)
        util.logger.info("Looks like you're all set up. Let's get going!"){% endif %}
    # TODO your journey starts here
