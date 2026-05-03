# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2026-05-04

### Added
- Added `github` as a new `ci_pipeline` option (closes #44). Selecting GitHub Actions generates `.github/workflows/ci.yml` with `build` and `test` jobs, supporting all four package managers (conda with micromamba, pip, poetry, uv). The GitLab CI option is unchanged.

### Changed
- Updated the README to document the new GitHub Actions CI choice under "Choices explained".

## [1.3.0] - 2026-01-27

### ⚠️ Breaking Changes
- **Minimum Python version increased from 3.9 to 3.10** (required for secure dependency versions)

### Security
- Fixed CVE-2024-47081: Updated `requests` from 2.32.3 to 2.32.5 (Moderate - .netrc credentials leak)
- Fixed CVE-2025-50181: Updated `urllib3` from 2.4.0 to 2.6.3 (Moderate - redirects not disabled with retries)
- Fixed CVE-2025-50182: Updated `urllib3` to 2.6.3 (Moderate - redirects in browsers/Node.js)
- Fixed CVE-2025-66418: Updated `urllib3` to 2.6.3 (High - unbounded decompression chain)
- Fixed CVE-2025-66471: Updated `urllib3` to 2.6.3 (High - improper handling of compressed data)
- Fixed CVE-2026-21441: Updated `urllib3` to 2.6.3 (High - decompression-bomb bypass in redirects)
- Fixed CVE-2026-24049: Updated `wheel` from 0.45.1 to 0.46.3 (High - path traversal in wheel unpack)
- Fixed CVE-2025-68146: Updated `filelock` from 3.18.0 to 3.20.3 (Moderate - TOCTOU symlink attack)
- Fixed CVE-2026-22701: Updated `filelock` to 3.20.3 (Moderate - TOCTOU in SoftFileLock)
- Fixed CVE-2026-22702: Updated `virtualenv` from 20.31.2 to 20.36.1 (Moderate - TOCTOU in directory creation)

### Changed
- Updated CI/CD workflows to test Python 3.10 and 3.13 (dropped 3.9)
- Updated all template files and documentation to reflect Python 3.10 minimum requirement
- Updated GitHub Actions `actions/setup-python` from v5 to v6
- Updated `cookiecutter` from 2.3 to 2.6
- Updated `pre-commit` from 4.3.0 to 4.5.1
- Updated `pytest` from 8.4.1 to 9.0.2
- Updated `pytest-cov` from 6.2.1 to 7.0.0
- Updated `pytest-mock` from 3.14.1 to 3.15.1
- Updated `pyyaml` from 6.0.2 to 6.0.3
- Updated `typer` from 0.16.1 to 0.21.1
- Updated `setuptools` from 80.9.0 to 80.10.2
- Updated pre-commit hook `astral-sh/ruff-pre-commit` from v0.12.10 to v0.14.14
- Updated pre-commit hook `pycqa/isort` from v6.0.1 to v6.1.0
- Updated pre-commit hook `asottile/pyupgrade` args from `--py39-plus` to `--py310-plus`
- Updated Python base images in GitLab CI from 3.9 to 3.10
- Fixed YAML parsing issue in GitHub Actions workflow (quoted Python versions to prevent 3.10 → 3.1)

### Dependency Updates (Transitive)
- Updated `arrow` from 1.3.0 to 1.4.0
- Updated `certifi` from 2025.4.26 to 2026.1.4
- Updated `cfgv` from 3.4.0 to 3.5.0
- Updated `charset-normalizer` from 3.4.2 to 3.4.4
- Updated `click` from 8.1.8 to 8.3.1
- Updated `coverage` from 7.8.2 to 7.13.2
- Updated `distlib` from 0.3.9 to 0.4.0
- Updated `exceptiongroup` from 1.3.0 to 1.3.1
- Updated `identify` from 2.6.12 to 2.6.16
- Updated `idna` from 3.10 to 3.11
- Updated `iniconfig` from 2.1.0 to 2.3.0
- Updated `markdown-it-py` from 3.0.0 to 4.0.0
- Updated `markupsafe` from 3.0.2 to 3.0.3
- Updated `nodeenv` from 1.9.1 to 1.10.0
- Updated `packaging` from 25.0 to 26.0
- Updated `platformdirs` from 4.3.8 to 4.5.1
- Updated `pygments` from 2.19.1 to 2.19.2
- Updated `pyparsing` from 3.2.3 to 3.3.2
- Updated `rich` from 14.0.0 to 14.3.1
- Updated `tomli` from 2.2.1 to 2.4.0
- Added `tzdata` 2025.3

### Summary
All 10 Dependabot security vulnerabilities have been resolved (4 High, 6 Moderate).
All dependencies updated to latest stable versions as of January 2026.


## [1.2.2] - 2025-08-22
### Changed
- Aktualisiert: pre-commit Hook `astral-sh/ruff-pre-commit` von `v0.11.12` auf `v0.12.10`.
- Aktualisiert: pre-commit Hook `pycqa/isort` von `v5.13.2` auf `v6.0.1`.
- Aktualisiert: Abhängigkeit `typer` von `0.16.0` auf `0.16.1`.
- Aktualisiert: Dev-Abhängigkeit `pytest` von `8.4.0` auf `8.4.1`.
- Updated pre-commit hook `astral-sh/ruff-pre-commit` from `v0.11.12` to `v0.12.10`.
- Updated pre-commit hook `pycqa/isort` from `v5.13.2` to `v6.0.1`.
- Updated dependency `typer` from `0.16.0` to `0.16.1`.
- Updated dev dependency `pytest` from `8.4.0` to `8.4.1`.
- Updated lock file (`poetry.lock`) to reflect new version states.

## [1.2.1] - 2025-06-05
### Changed

- Updated pytest from 8.3.4 to 8.4
- Updated typer from 0.15.1 to 0.16.0
- Updated pre-commit hook assotile/pyugrade from v3.19.1 to v3.20.0
- Updated setuptools from 76.0.0 to 80.9.0
- Updated Python Docker tags from 3.11-slim-bookworm to 3.13-slim-bookworm and 3.11-bullseye to 3.13-bullseye
- Updated pre-commit ruff from v0.11.0 to v0.11.12

## [1.2.0] - 2025-04-09

### Added
- Introduced support for a new package manager `uv` in `cookiecutter.json`, `hooks/post_gen_project.py`, and `README.md`.
- Added `Dockerfile__uv` for `uv` package manager support.

### Changed
- Updated project version from `1.1.1` to `1.2.0` in `pyproject.toml`.
- Updated `ruff` pre-commit hook from `v0.9.10` to `v0.11.0` in `.pre-commit-config.yaml`.
- Updated `ruff` dependency in `environment-dev.yml` from `>=0.9.7` to `>=0.11.0`.
- Updated `pytest` from `^8.3.4` to `^8.3.5` in `pyproject.toml`.
- Updated `ruff` from `^0.9.7` to `^0.11.0` in `pyproject.toml`.
- Updated `black` from `~22.10` to `~25.1.0` in `requirements-dev.txt`.
- Updated `pytest` from `~8.3` to `~8.3.5` in `requirements-dev.txt`.
- Updated `wheel` from `~0.37` to `~0.45.1` in `requirements-dev.txt`.

### Documentation
- Added detailed instructions for using `uv` package manager in `README.md`, including installation, dependency management, running scripts, and testing.
- Updated the README with new commands for `uv`, `poetry`, and `pip` package managers for running tests, building distribution packages, and setting up pre-commit hooks.

### Fixed
- Corrected minor formatting issues in the `pyproject.toml` and `README.md`.

### Other
- Updated `.dockerignore` to include additional directories and files.
- Updated `docker-compose.yml` to support `uv` package manager.
- Updated `requirements-dev.txt` for `black`, `pytest`, and `wheel` versions.

## [1.1.1] - 2025-03-13

### Changed
- Updated dependency `setuptools` to v76.
- Updated dependency `pytest` to v8.3.5.
- Updated dependency `typer` to v0.15.2.
- Updated pre-commit hook `astral-sh/ruff-pre-commit` to v0.9.10.


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
- Updated versions of GitLab CI python and poetry versions.
- Fixed pre-commit hook for `black` installation via pip with the correct version constraint (`>=`).

### Fixed

- Fixed test since `black` is installed by pip, and updated the test to check for the correct version format (`>=`).
- Fixed coverage reporting integration in GitHub Actions.

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

[Unreleased]: https://github.com/at-gmbh/at-python-template/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/at-gmbh/at-python-template/compare/v1.2.2...v1.3.0
[1.2.2]: https://github.com/at-gmbh/at-python-template/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/at-gmbh/at-python-template/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/at-gmbh/at-python-template/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/at-gmbh/at-python-template/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/at-gmbh/at-python-template/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/at-gmbh/at-python-template/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/at-gmbh/at-python-template/releases/tag/v1.0.0
