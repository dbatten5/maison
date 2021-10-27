[![Actions Status](https://github.com/dbatten5/maison/workflows/Tests/badge.svg)](https://github.com/dbatten5/maison/actions)
[![Actions Status](https://github.com/dbatten5/maison/workflows/Release/badge.svg)](https://github.com/dbatten5/maison/actions)
[![codecov](https://codecov.io/gh/dbatten5/maison/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/dbatten5/maison)

# Maison

Read configuration settings from `python` configuration files.

## Motivation

When developing a `python` application, e.g a command-line tool, it can be
helpful to allow the user to set their own configuration options to allow them
to tailor the tool to their needs. These options are typically set in files in
the root of a project directory that uses the tool, for example in a
`pyproject.toml` file.

`maison` aims to provide a simple and flexible way to read and validate those
configuration options so that they may be used in the application.

## Installation

```bash
pip install maison
```

## Usage

Suppose the following `pyproject.toml` lives somewhere in a project directory:

```toml
[tool.acme]
new_lines = true
```

`maison` exposes a `ProjectConfig` class to retrieve values from config files
like so:

```python
from maison import ProjectConfig

config = ProjectConfig(project_name="acme")

if config.get_option("new_lines"):
    # make sure to add new lines
```

## Help

See the [documentation](https://dbatten5.github.io/maison) for more details.

## Licence

MIT
