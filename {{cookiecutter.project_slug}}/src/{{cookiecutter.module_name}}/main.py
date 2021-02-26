import logging

from {{ cookiecutter.module_name }} import util

logger = logging.getLogger('{{ cookiecutter.module_name }}')


def main():
    {% if cookiecutter.config_file != 'none' -%}
    config = util.load_config({% if cookiecutter.config_file == 'yaml' %}'config/config.yml'{% else %}None{% endif %})
    util.logging_setup(config)
    {% else -%}
    logging.basicConfig(level=logging.INFO)
    {% endif -%}
    logger.info("Looks like you're all set up. Let's get going!")
    # TODO your journey starts here


if __name__ == "__main__":
    main()
