#!/usr/bin/env python3
# pylint: disable=invalid-name
""" Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""
import sphinx_bootstrap_theme
author = 'Rudy Attias, Steve Moore, Xander Harris'
autoyaml_root = '..'
autoyaml_level = 10

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_bootstrap_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.duration',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.autoyaml',
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

myst_enable_extensions = [
    "amsmath",
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_footnote_transition=True
myst_title_to_header=True


project = 'K8s Operator Agent'
project_copyright = '2024, Rudy Attias, Steve Moore, Xander Harris'
release = '0.0.1'

show_authors=True
source_suffix = {
    '.md': 'markdown',
}

templates_path = ['_templates']
