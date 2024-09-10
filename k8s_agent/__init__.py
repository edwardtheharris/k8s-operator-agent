"""Kubernetes Agent module."""
from pathlib import Path

import version_query

def get_version():
    """Query the current version for the project."""
    try:
        repo_path = Path(".").resolve()
        ret_value = version_query.git_query.query_git_repo(repo_path).to_str()
    except ValueError:
        ret_value = version_query.Version.from_str('0.0.0')
        ret_value = ret_value.devel_increment()
    return ret_value

__version__ = get_version()
