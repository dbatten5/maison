[![Actions Status](https://github.com/dbatten5/maison/workflows/Tests/badge.svg)](https://github.com/dbatten5/maison/actions)
[![Actions Status](https://github.com/dbatten5/maison/workflows/Release/badge.svg)](https://github.com/dbatten5/maison/actions)
[![Coverage Status](https://coveralls.io/repos/github/dbatten5/maison/badge.svg?branch=master)](https://coveralls.io/github/dbatten5/maison?branch=main)

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

# Usage

!!! warning ""
    Currently only reading from a `pyproject.toml` is supported

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

`maison` searches for config files by starting at `Path.cwd()` and moving up
the tree until it finds a `pyproject.toml` or there are no more parent paths.

You can start searching from a different path by providing a `starting_path`
init variable to `ProjectConfig`.

You can also provide an optional second argument to `.get_option` which will
be returned if the given option isn't found. For example in the above example:

```python
config.get_option("baz", "default") # returns "default"
```
