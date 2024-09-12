#!/usr/bin/env python3
"""Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""
# pylint: disable=invalid-name,redefined-builtin
import sys
from pathlib import Path
import version_query

sys.path.append(str(Path("./k8s_agent").resolve()))
sys.path.append(str(Path(".").resolve()))


def get_release():
    """Query the current release for the project."""
    try:
        repo_path = Path(".")
        ret_value = version_query.git_query.query_git_repo(repo_path).to_str()
    except ValueError:
        ret_value = "0.0.1"
    return ret_value


author = "Rudy Attias"
autoyaml_root = "."
autoyaml_doc_delimiter = "###"
autoyaml_comment = "#"
autoyaml_level = 10
autoyaml_safe_loader = True
copyright = "2024, Rudy Attias"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    "requirements.txt",
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv/*",
    ".tmp/*",
    ".pytest_cache/*",
    "deployment/helm/k8s-agent/templates/NOTES.txt",
    "resources/templates/NOTES.txt",
]

extensions = [
    "myst_parser",
    "sphinx_design",
    'sphinx.ext.autodoc',
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.autoyaml",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = "_static/img/logo/k8s-operator-agent.jpg"
html_favicon = "_static/img/logo/k8s-operator-agent.jpg"
html_static_path = ["_static"]
html_theme = "sphinx_book_theme"
intersphinx_mapping = {
    'asyncio': ('https://pytest-asyncio.readthedocs.io/en/latest/', None),
    'hypercorn': ('https://hypercorn.readthedocs.io/en/latest/', None),
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None)
}
myst_dmath_double_inline = True
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
myst_title_to_header = True
project = "Template Helm Chart"
rst_epilog = """
.. sectionauthor:: Xander Harris <xandertheharris@gmail.com>
"""
release = get_release()
show_authors = True
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
    ".txt": "markdown",
}
templates_path = ["_templates"]
