"""Sphinx configuration."""

project = "Maison"
author = "Dom Batten"
copyright = "2025, Dom Batten"  # noqa

release = "2.0.0"
version = ".".join(release.split(".")[:2])

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxcontrib.typer",
    "myst_parser",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]
templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    ".nox",
    "rust",
    "tests",
    "cookiecutter.json",
    "README.md",
    "noxfile.py",
    ".pre-commit-config.yaml",
    "pyproject.toml",
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
    "attrs_inline",
    "attrs_block",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_theme = "furo"
