# Contributing to AT Python Template

We welcome your contributions! Whether it's reporting a bug, discussing ideas, submitting fixes, or proposing new features, we appreciate your input.

## We Develop with GitHub
We use GitHub to host code, track issues, and review pull requests.

## Follow the GitHub Flow
All changes should be proposed through pull requests:

1. Fork the repository and create your branch from `master`.
2. If you've added new functionality, include tests.
3. Update the documentation if there are any changes to APIs or usage.
4. Ensure all tests pass.
5. Verify that your code adheres to linting and formatting standards.
6. Submit your pull request!

## Code License
When you submit code changes, you agree that your contributions will be licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Reporting Issues
Please use [GitHub Issues](https://github.com/at-gmbh/at-python-template/issues) to report bugs and suggest improvements. Make sure to include:

- A brief summary of the issue
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Additional notes or related references

## Coding Standards

- Use 4 spaces per indentation level
- Maximum line length is 120 characters
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Ruff](https://github.com/charliermarsh/ruff) for formatting and linting (applied automatically with pre-commit hooks, or manually if needed)
- Include type hints as per [PEP 484](https://peps.python.org/pep-0484/)
- Use Google-style docstrings
- Ensure code is clean, readable, and maintainable

## Imports

- Order imports as follows:
  1. Future imports
  2. Standard library imports
  3. Third-party imports
  4. Local imports
- Avoid wildcard imports
- Use absolute imports unless relative imports simplify the code

## Comments

- Write comments in English
- Explain the intention behind code, not what the code does
- Use full sentences with proper capitalization and punctuation

## Naming Conventions

- Variables and functions: `lower_case_with_underscores`
- Classes: `CapWords`
- Constants: `ALL_CAPS_WITH_UNDERSCORES`
- Modules: `alllowercase`

## Setting Up for Development

1. Install dependencies using `poetry install`.
2. Run tests with `pytest tests`.
3. Use `pre-commit install` to set up pre-commit hooks. This ensures that Ruff and other checks run before each commit.

## Testing
We use [pytest](https://docs.pytest.org/) for running tests. Ensure that all tests pass before submitting a pull request.

## Additional Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Poetry Documentation](https://python-poetry.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Thank you for your contributions!
