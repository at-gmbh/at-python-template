# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Placeholder for future updates and new features.
-
## [1.0.1] - 2025-02-26
### Fixed
- **Conda package caching in GitLab CI:** Updated caching paths in `{{ cookiecutter.project_slug }}/.gitlab-ci.yml` to include the new `.conda` file format and additional cache directories. The updated paths now cache:
  - `$PIP_CACHE_DIR`
  - `$CONDA_PKGS_DIRS/*.conda`
  - `$CONDA_PKGS_DIRS/*.tar.bz2`
  - `$CONDA_PKGS_DIRS/urls*`
  - `$CONDA_PKGS_DIRS/cache`

  This change ensures that all relevant Conda packages and related metadata are properly cached, addressing issues with the previous configuration ([Conda docs](https://conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html#force-conda-to-download-only-tar-bz2-packages-use-only-tar-bz2), [Damiankula’s guide](https://damiankula.com/using_conda_cache_in_gitlabci.html)). cc @ChrsBaur

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
