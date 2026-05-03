import logging
from {{ cookiecutter.module_name }} import util

logger = logging.getLogger('{{ cookiecutter.module_name }}')


def main():
    util.setup_logging()
    logger.info("Looks like you're all set up. Let's get going!")
    # TODO your journey starts here


if __name__ == "__main__":
    main()
