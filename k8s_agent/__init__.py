"""Kubernetes Agent module.


This module provides utilities for querying the version of the project
from a Git repository and handling versioning for the Kubernetes agent.
"""
from pathlib import Path

import version_query

def get_version():
    """Query the current version for the project.

    This function retrieves the current version of the project from
    the Git repository using `version_query`. If the version cannot be
    retrieved (e.g., if the repository is not valid), a default version
    of `0.0.0` is used, and a development increment is added.

    :var Path repo_path: The full path to the current directory.
    :var str ret_value: The current or next version of the project.
    :return str: A semantic version for the repository.
    """
    try:
        repo_path = Path(".").resolve()
        ret_value = (
            version_query.git_query
            .query_git_repo(repo_path)
            .to_str()
        )
    except ValueError:
        ret_value = version_query.Version.from_str('0.0.0')
        ret_value = ret_value.devel_increment()
    return ret_value

__version__ = get_version()
