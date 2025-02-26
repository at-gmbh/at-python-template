# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-02-26

### Added

- Adjusted Python version to be at least 3.9 in `pyproject.toml` and `environment-dev.yml`.
- Adjusted GitHub Actions to only use `poetry` for dependency management.
- Refactored utility code by replacing `pkg_resources` with `importlib.resources`.
- Added support for `pytest-cov` v6.
- Added test coverage reporting to the GitHub Actions pipeline.
- Updated Conda Docker tag to `v24` in `Dockerfile`.
- Updated `actions/checkout` GitHub action to v4.
- Updated pre-commit hooks, including:
  - `pycqa/isort` to v5.13.2.
  - `pre-commit/pre-commit-hooks` to v4.6.0.
  - `astral-sh/ruff-pre-commit` to v0.9.7.
  - `asottile/pyupgrade` to v3.19.1.
- Updated `requirements.txt` in the cookiecutter project.
- Made use of Python 3.9 and newer versions in `pyproject.toml`.
- Upgraded dependencies in `pyproject.toml` to ensure the project uses the latest versions.
- Updated and aligned `environment-dev.yml` and `environment.yml` with `pyproject.toml` for consistency.
- Updated versions of GitLab CI YAML files.
- Fixed pre-commit hook for `black` installation via pip with the correct version constraint (`>=`).

### Fixed

- Fixed test since `black` is installed by pip, and updated the test to check for the correct version format (`>=`).
- Fixed coverage reporting integration in GitHub Actions.

## [1.0.0] - 2025-02-26

### Added
- **Initial stable release** of the AT Python Template.
- **Modular project structure** using `src/` directory for better code organization.
- **Flexible package management** with options for `pip`, `poetry`, and `conda`.
- **Automated project setup** using `cookiecutter` to streamline project generation.
- **Pre-configured CLI support** via `typer`, enabling command-line applications.
- **Pre-commit hooks** with `ruff` for formatting and linting.
- **Docker integration** with `Dockerfile` and `docker-compose.yml` for containerized deployment.
- **Automated testing setup** using `pytest` for unit testing.
- **Jupyter Notebook compatibility** with a dedicated `notebooks/` folder.
- **Configuration management** using `config/` directory and YAML/HOCON formats.
- **Editor support** with settings for **VS Code** and **PyCharm**.
- **Multiple CI/CD integrations** including **GitHub Actions** and **GitLab CI**.
- **Automated dependency updates** using `renovate`.
- **Updated documentation** covering installation, project structure, and setup steps.
- **Human-readable prompts** improving user experience during project generation.
- **Versioning enforcement** requiring **Python 3.8+** while dropping Python 3.7 support.

### Changed
- **Refactored codebase** to ensure maintainability and modularity.
- **Updated default dependencies** for better performance and security.
- **Enhanced user prompts** for a more intuitive project setup.
- **Switched to f-strings** replacing old `.format()` calls for improved readability.
- **Simplified installation steps** by improving `README.md` structure.
- **Improved GitHub Actions workflows** for automated testing and validation.

### Fixed
- **Resolved setup issues** related to module placement under `src/`.
- **Fixed broken paths and URLs** in documentation.
- **Ensured pre-commit hooks work as expected** with proper configurations.
- **Addressed whitespace inconsistencies** in generated files.

---

[Unreleased]: https://github.com/at-gmbh/at-python-template/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/at-gmbh/at-python-template/releases/tag/v1.0.0
