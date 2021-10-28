# Retrieving values

Once an instance of `ProjectConfig` has been created, values can be retrieved through:

```python
>>> config.get_option("foo")
'bar'
```

An optional second argument can be provided to `get_option` which will be returned if
the given option isn't found:

```python
>>> config.get_option("baz", "default")
'default'
```

`ProjectConfig` also exposes a `to_dict()` method to return all the config
options:

```python
>>> config.to_dict()
{'foo': 'bar'}
```

# Source files

By default, `maison` will look for a `pyproject.toml` file. If you prefer to look
elsewhere, provide a `source_files` list to `ProjectConfig` and `maison` will select the
first source file it finds from the list. Note that there is no merging of configs.


```python
from maison import ProjectConfig

config = ProjectConfig(
  project_name="acme",
  source_files=["acme.ini", "pyproject.toml"]
)

print(config)
# ProjectConfig (config_path=/path/to/acme.ini)
```

!!! warning ""
    Currently only `.toml` and `.ini` files are supported. For `.ini` files,
    `maison` assumes that the whole file is relevant. For `.toml` files,
    `maison` assumes that the relevant section will be in a
    `[tool.{project_name}]` section.

To verify which source config file has been found, `ProjectConfig` exposes a
`config_path` property:

```python
>>> config.config_path
PosixPath('/path/to/pyproject.toml')
```

# Search paths

By default, `maison` searches for config files by starting at `Path.cwd()` and moving up
the tree until it finds the relevant config file or there are no more parent paths.

You can start searching from a different path by providing a `starting_path` property to
`ProjectConfig`:

```python
from maison import ProjectConfig

config = ProjectConfig(
  project_name="acme",
  starting_path=Path("/some/other/path")
)

print(config)
# ProjectConfig (config_path=/some/other/path/pyproject.toml)
```
