"""Kubernetes Operator Agent init test module."""
# pylint: disable=redefined-outer-name,reimported,import-outside-toplevel
from unittest.mock import patch
from unittest.mock import MagicMock

import version_query

from k8s_agent import get_version
from k8s_agent import __version__

def test_get_version_success():
    """Test get_version when git version query is successful.

    Mock the return value of query_git_repo to simulate successful
    version retrieval.
    """

    mock_version = MagicMock()
    mock_version.to_str.return_value = "1.2.3"

    with patch("k8s_agent.version_query.git_query.query_git_repo",
               return_value=mock_version):
        version = get_version()
        assert version == "1.2.3"
        mock_version.to_str.assert_called_once()

def test_get_version_fallback():
    """Test get_version failure back to default version.

    Mock the query_git_repo to raise a ValueError

    Mock the Version.from_str and its devel_increment behavior
    """
    with patch("k8s_agent.version_query.git_query.query_git_repo",
               side_effect=ValueError):
        mock_version = MagicMock()
        mock_version.devel_increment.return_value = "0.0.1"

        with patch("k8s_agent.version_query.Version.from_str",
                   return_value=mock_version):
            version = get_version()
            assert version == "0.0.1"
            mock_version.devel_increment.assert_called_once()

def test_version_init():
    """Test if __version__ is initialized correctly."""
    with patch("k8s_agent.get_version", return_value="1.2.3"):
        from k8s_agent import __version__
        assert __version__ == version_query.Version.from_str("0.0.1.dev1")
