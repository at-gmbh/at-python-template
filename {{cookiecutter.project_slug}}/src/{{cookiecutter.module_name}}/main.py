{% if cookiecutter.config_file != 'none' %}{% if cookiecutter.config_file == 'yaml' %}import os
{% endif %}import logging
from {{ cookiecutter.module_name }} import util

logger = logging.getLogger("{{ cookiecutter.module_name }}")

{% endif %}
def main():
    {% if cookiecutter.config_file != 'none' %}config = util.load_config({% if cookiecutter.config_file == 'yaml' %}os.path.join(os.path.abspath(__file__),
                                           *[os.pardir]*3,
                                           "config",
                                           "config.yml"){% endif %})
    util.logging_setup(config)

    logger.info("Looks like you're all set up. Let's get going!")

    {% endif %}# TODO your journey starts here
    print("hello :)")


if __name__ == "__main__":
    main()
