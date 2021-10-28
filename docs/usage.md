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

# Validation

`maison` offers optional schema validation using [pydantic](https://pydantic-docs.helpmanual.io/).

To validate a configuration, first create a schema which subclasses `ConfigSchema`:

```python
from maison import ConfigSchema

class MySchema(ConfigSchema):
  foo: str = "my_default"
```

!!! note ""
    `ConfigSchema` offers all the same functionality as the `pydantic` [BaseModel](https://pydantic-docs.helpmanual.io/usage/models/)

Then inject the schema when instantiating a `ProjectConfig`:

```python
from maison import ProjectConfig

config = ProjectConfig(project_name="acme", schema=MySchema)
```

To validate the config, simply run `validate()` on the config instance:

```python
config.validate()
```

If the configuration is invalid, a `pydantic` `ValidationError` will be raised. If the
configuration is valid, nothing will happen.

## Casting and default values

By default, `maison` will replace the values in the config with whatever comes back from
the validation. For example, for a config file that looks like this:

```toml
[tool.acme]
foo = 1
```

And a schema that looks like this:

```python
class MySchema(ConfigSchema):
  foo: str
  bar: str = "my_default"
```

Running the config through validation will render the following:

```python
config = ProjectConfig(project_name="acme", schema=MySchema)

config.to_dict() # {"foo": 1}

config.validate()
config.to_dict() # {"foo": "1", "bar": "my_default"}
```

If you prefer to keep the config values untouched and just perform simple validation,
add a `use_schema_values=False` argument to the `validate` method.

## Schema precedence

The `validate` method also accepts a `schema` is an argument. If one is provided here,
it will be used instead of a schema passed as an init argument.
