[![Actions Status](https://github.com/dbatten5/maison/workflows/Tests/badge.svg)](https://github.com/dbatten5/maison/actions)
[![Actions Status](https://github.com/dbatten5/maison/workflows/Release/badge.svg)](https://github.com/dbatten5/maison/actions)
[![codecov](https://codecov.io/gh/dbatten5/maison/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/dbatten5/maison)

When developing a `python` application, e.g a command-line tool, it can be
helpful to allow the user to set their own configuration options to allow them
to tailor the tool to their needs. These options are typically set in files in
the root of a project directory that uses the tool, for example in a
`pyproject.toml` file.

`maison` aims to provide a simple and flexible way to read and validate those
configuration options so that they may be used in the application.

# Installing

```bash
pip install maison
```

# Example

Suppose we have a `pyproject.toml` which looks like the following:

```toml
[tool.acme]
foo = "bar"
```

In order to read the value of `foo`, run the following:

```python
from maison import ProjectConfig

config = ProjectConfig(project_name="acme")
config.get_option("foo") # returns "bar"
```
