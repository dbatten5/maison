# Maison

[![Actions Status](https://github.com/dbatten5/maison/workflows/Tests/badge.svg)](https://github.com/dbatten5/maison/actions)
[![Actions Status](https://github.com/dbatten5/maison/workflows/Release/badge.svg)](https://github.com/dbatten5/maison/actions)
[![codecov](https://codecov.io/gh/dbatten5/maison/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/dbatten5/maison)
[![PyPI version](https://badge.fury.io/py/maison.svg)](https://badge.fury.io/py/maison)

Read configuration settings from configuration files.

## Motivation

When developing a `python` application, e.g a command-line tool, it can be
helpful to allow the user to set their own configuration options to allow them
to tailor the tool to their needs. These options are typically set in files in
the root of a project directory that uses the tool, for example in a
`pyproject.toml` or an `{project_name}.ini` file.

`maison` aims to provide a simple and flexible way to read and validate those
configuration options so that they may be used in the application.

### Features

- Supports multiple config files and multiple config filetypes.
- Optional merging of multiple configs.
- Optional config validation with [pydantic](https://pydantic-docs.helpmanual.io/).
- Caching of config files for quick access.
- Fully tested and typed.

## Installation

```bash
pip install maison
```

## Usage

Suppose the following `pyproject.toml` lives somewhere in a project directory:

```toml
[tool.acme]
enable_useful_option = true
```

`maison` exposes a `ProjectConfig` class to retrieve values from config files
like so:

```python
from maison import ProjectConfig

config = ProjectConfig(project_name="acme")

if config.get_option("enable_useful_option"):
    # include the useful option
```

## Help

See the [documentation](https://dbatten5.github.io/maison) for more details.

## Licence

MIT
