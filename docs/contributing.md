# Issues

If you notice an issue with `maison` or would like to suggest a feature or just
have a general question, please raise an
[issue](https://github.com/dbatten5/maison/issues) on GitHub. If it's an issue
that needs debugging please make sure to include the version of `maison` in the
issue description. You can retrieve the version with the following:

```bash
pip freeze | grep maison
```

# Pull Requests

If you would like to contribute to the repo, you would be most welcome. If
you're tackling an existing issue please comment on the issue that you'd like to
take it on. If it's a new feature/bug, please first raise an issue. There is
also a `kanban` board [here](https://github.com/dbatten5/maison/projects/1) for
more feature ideas.

# Local Development

In order to work on your contribution, you'll need to first fork the repo and
then clone it to your local machine:

```bash
git clone git@github.com:<your username>/maison.git
cd maison
```

You'll need `python` 3.6, 3.7, 3.8 or 3.9 to run this package. You can follow
the instructions [here](https://cookiecutter-hypermodern-python.readthedocs.io/en/2021.6.15/guide.html#getting-python)
to install and use these versions.

This package uses `poetry` to manage dependencies. Ensure you have `poetry`
installed, instructions [here](https://python-poetry.org/docs/#installation) and
run:

```bash
poetry install
```

This will install the dependencies into a `.venv` virtual environment. You can
activate the env with either `source .venv/bin/activate` or `poetry shell`.

Next install the `pre-commit` hooks with:

```bash
pre-commit install
```

[Nox](https://nox.thea.codes/en/stable/) is used to run tests, linters, type
checkers etc. These are all run in the CI and on `git commit` but if you'd like
to run them manually, you can do so with, eg:

```bash
nox --session=tests
```

This will run the tests for all versions of python.

See [here](https://cookiecutter-hypermodern-python.readthedocs.io/en/2021.6.15/guide.html#running-sessions)
for more information on running `nox` locally.

If you're making changes that will require updates to the documentation, please
do so accordingly. Documentation lives in the `docs/` directory and can be
served locally with:

```bash
mkdocs serve
```

See [here](https://squidfunk.github.io/mkdocs-material/getting-started/) for
more information on working with `mkdocs`.

Once you're ready with your shiny, TDD'd feature, commit, push, and open a pull
request and I'll be happy to review. If you're having issues with any of this
setup please do let me know and I'll try and help.
