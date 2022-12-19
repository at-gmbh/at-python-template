{% if cookiecutter.config_file == 'hocon' %}import os
from pyhocon import ConfigFactory

{% endif %}def main():
    # TODO your journey starts here
    {% if cookiecutter.config_file == 'hocon' %}config = ConfigFactory.parse_file(f"config/{os.environ['ENV']}.conf")
    print(f"hello {config.get('username')} :)"){% else %}print("hello :)"){% endif %}


if __name__ == "__main__":
    main()
