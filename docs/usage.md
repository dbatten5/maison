# Usage

Suppose a `pyproject.toml` file lives in the user's directory:

```toml
[tool.acme]
foo = "bar"
```

## Retrieving values

`UserConfig` objects behave like dicts and config values can be retrieved as if
they were dict values:

```python
>>> from maison import UserConfig
>>> config = UserConfig(project_name="acme")
>>> config
"{'foo': 'bar'}"
>>> config["foo"]
'bar'
>>> "baz" in config
False
>>> config.get("baz", "qux")
'qux'
```

## Source files

By default, `maison` will look for a `pyproject.toml` file. If you prefer to look
elsewhere, provide a `source_files` list to `UserConfig` and `maison` will select the
first source file it finds from the list.

```python
from maison import UserConfig

config = UserConfig(
  project_name="acme",
  source_files=["acme.ini", "pyproject.toml"]
)

print(config.config_path)
#> PosixPath(/path/to/acme.ini)
```

```{caution}
Currently only `.toml` and `.ini` files are supported. For `.ini` files,
`maison` assumes that the whole file is relevant. For `pyproject.toml` files,
`maison` assumes that the relevant section will be in a
`[tool.{project_name}]` section. For other `.toml` files `maison` assumes the whole
file is relevant.
```

To verify which source config file has been found, `UserConfig` exposes a
`config_path` property:

```python
>>> config.config_path
PosixPath('/path/to/pyproject.toml')
```

The source file can either be a filename or an absolute path to a config:

```python
from maison import UserConfig

config = UserConfig(
  project_name="acme",
  source_files=["~/.config/acme.ini", "pyproject.toml"]
)

print(config.config_path)
#> PosixPath(/Users/tom.jones/.config/acme.ini)
```

## Merging configs

`maison` offers support for merging multiple configs. To do so, set the `merge_configs`
flag to `True` in the constructor for `UserConfig`:

```python
from maison import UserConfig

config = UserConfig(
  project_name="acme",
  source_files=["~/.config/acme.toml", "~/.acme.ini", "pyproject.toml"],
  merge_configs=True
)

print(config.config_path)
"""
[
  PosixPath(/Users/tom.jones/.config/acme.toml),
  PosixPath(/Users/tom.jones/.acme.ini),
  PosixPath(/path/to/pyproject.toml),
]
"""

print(config.get_option("foo"))
#> "bar"
```

```{warning}
When merging configs, `maison` merges from **right to left**, ie. rightmost sources
take precedence. So in the above example, if `~/config/.acme.toml` and
`pyproject.toml` both set `nice_option`, the value from `pyproject.toml` will be
returned from `config.get_option("nice_option")`.
```

## Search paths

By default, `maison` searches for config files by starting at `Path.cwd()` and moving up
the tree until it finds the relevant config file or there are no more parent paths.

You can start searching from a different path by providing a `starting_path` property to
`UserConfig`:

```python
from maison import UserConfig

config = UserConfig(
  project_name="acme",
  starting_path=Path("/some/other/path")
)

print(config.config_path)
#> PosixPath(/some/other/path/pyproject.toml)
```

## Validation

`maison` offers optional schema validation.

To validate a configuration, first create a schema. The schema should implement
a method called `dict`. This can be achieved by writing the schema as a
`pydantic` model:

```python
from maison import ConfigSchema
from pydantic import BaseModel

class MySchema(BaseModel):
  foo: str = "my_default"
```

```{note}
`maison` validation was built with using `pydantic` models as schemas in mind
but this package doesn't explicitly declare `pydantic` as a dependency so you
are free to use another validation package if you wish, you just need to ensure
that your schema follows the `maison.config.IsSchema` protocol.
```

Then inject the schema when instantiating a `UserConfig`:

```python
from maison import UserConfig

config = UserConfig(project_name="acme", schema=MySchema)
```

To validate the config, simply run `validate()` on the config instance:

```python
config.validate()
```

If the configuration is invalid and if you are using a `pydantic` base model as
your schema, a `pydantic` `ValidationError` will be raised. If the configuration
is valid, the validated values are returned.

If `validate` is invoked but no schema has been provided, a `NoSchemaError` will
be raised. A schema can be added after instantiation through a setter:

```python
config.schema = MySchema
```

## Casting and default values

By default, `maison` will replace the values in the config with whatever comes back from
the validation. For example, for a config file that looks like this:

```toml
[tool.acme]
foo = 1
```

And a schema that looks like this:

```python
class MySchema(BaseModel):
  foo: str
  bar: str = "my_default"
```

Running the config through validation will render the following:

```python
config = UserConfig(project_name="acme", schema=MySchema)

print(config)
#> {"foo": 1}

config.validate()
print(config)
#> {"foo": "1", "bar": "my_default"}
```

If you prefer to keep the config values untouched and just perform simple validation,
add a `use_schema_values=False` argument to the `validate` method.

### Schema precedence

The `validate` method also accepts a `config_schema` is an argument. If one is provided here,
it will be used instead of a schema passed as an init argument.
