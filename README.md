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

## Help

See the [documentation](https://dbatten5.github.io/maison) for more details.

## Installation

```bash
pip install maison
```

## Licence

MIT
