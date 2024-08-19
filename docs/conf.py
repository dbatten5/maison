"""Sphinx configuration."""

project = "Maison"
author = "Dom Batten"
copyright = "2021, Dom Batten"  # noqa: A001
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
