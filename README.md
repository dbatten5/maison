# Maison

[![Actions Status](https://github.com/dbatten5/maison/workflows/Tests/badge.svg)](https://github.com/dbatten5/maison/actions)
[![Actions Status](https://github.com/dbatten5/maison/workflows/Release/badge.svg)](https://github.com/dbatten5/maison/actions)
[![codecov](https://codecov.io/gh/dbatten5/maison/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/dbatten5/maison)
[![PyPI version](https://badge.fury.io/py/maison.svg)](https://badge.fury.io/py/maison)

Read configuration settings from configuration files.

**[📚 View Documentation](https://maison.readthedocs.io/)** | **[🐛 Report a Bug](https://github.com/dbatten/maison/issues)** | **[✨ Request a Feature](https://github.com/dbatten/maison/issues)**

---

## Motivation

When developing a `python` package, e.g a command-line tool, it can be helpful
to allow the user to set their own configuration options to allow them to tailor
the tool to their needs. These options are typically set in files in the root of
a user's directory that uses the tool, for example in a `pyproject.toml` or an
`{project_name}.ini` file.

`maison` aims to provide a simple and flexible way to read and validate those
configuration options so that they may be used in the package.

### Features

- Supports multiple config files and multiple config filetypes.
- Optional merging of multiple configs.
- Optional config validation with [pydantic](https://pydantic-docs.helpmanual.io/).
- Caching of config files for quick access.
- Fully tested and typed.

## Installation

You can install `maison` via [pip](pip-documentation) from PyPI:

```bash
pip install maison
```

### Installation for Development

To set up `maison` for local development:

1.  Clone the repository:
    ```bash
    git clone https://github.com/dbatten/maison.git
    cd maison
    ```
2.  Install dependencies using [:term:`uv`](uv-documentation):
    ```bash
    uv sync
    ```
3.  Install pre-commit hooks:
    ```bash
    uvx nox -s pre-commit -- install
    ```

This sets up a virtual environment and installs core, development, and quality check dependencies.

## Usage

Suppose the following `pyproject.toml` lives somewhere in a user's directory:

```toml
[tool.acme]
enable_useful_option = true
```

`maison` exposes a `UserConfig` class to retrieve values from config files
like so:

```python
from maison import UserConfig

from my_useful_package import run_useful_action

config = UserConfig(package_name="acme")

if config.values["enable_useful_option"]:
    run_useful_action()
```

## Development Workflow

This project uses a robust set of tools for development, testing, and quality assurance. All significant automated tasks are run via [:term:`Nox`](nox-documentation), orchestrated by the central `noxfile.py`.

- **Run all checks (lint, typecheck, security):** `uvx nox -s check`
- **Run test suite with coverage:** `uvx nox -s test`
- **Build documentation:** `uvx nox -s docs`
- **Build package:** `uvx nox -s build`
- **See all available tasks:** `uvx nox -l`

Explore the `noxfile.py` and the project documentation for detailed information on the automated workflow.

## Contributing

(This section should guide contributions _to this specific generated project_, not the template. It should refer to the project's `CODE_OF_CONDUCT.md` and link to a `CONTRIBUTING.md` specific to the project, if you choose to generate one.)

Report bugs or suggest features via the [issue tracker](https://github.com/dbatten/maison/issues).

See [CONTRIBUTING.md](#) for contribution guidelines.

## License

Distributed under the terms of the **MIT** license. See [LICENSE](LICENSE) for details.

---

**This project was generated from the [cookiecutter-robust-python template][cookiecutter-robust-python].**

<!-- Reference Links -->

[cookiecutter-robust-python]: https://github.com/56kyle/cookiecutter-robust-python
[documentation]: https://maison.readthedocs.io/
