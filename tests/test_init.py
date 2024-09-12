"""Kubernetes Operator Agent init test module."""
# pylint: disable=redefined-outer-name,reimported,import-outside-toplevel
from unittest.mock import patch
from unittest.mock import MagicMock

import version_query

from k8s_agent import get_version
from k8s_agent import __version__

def test_get_version_success():
    """Test get_version when git version query is successful.

    This test mocks the return value of `query_git_repo` to simulate
    successful version retrieval. It checks whether the version is
    returned correctly and verifies that the `to_str` method is called
    once.

    :var MagicMock mock_version: A MagicMock of the ``version_query`` module.
    :var str version: A string representation of the test version.
    """

    mock_version = MagicMock()
    mock_version.to_str.return_value = "1.2.3"

    with patch("k8s_agent.version_query.git_query.query_git_repo",
               return_value=mock_version):
        version = get_version()
        assert version == "1.2.3"
        mock_version.to_str.assert_called_once()

def test_get_version_fallback():
    """Test get_version fallback to default version on error.

    This test simulates a failure in retrieving the version from the Git
    repository by raising a `ValueError`. It mocks the `Version.from_str`
    method and its `devel_increment` behavior to verify that the default
    version ("0.0.1") is used when the Git query fails.

    :var MagicMock mock_version:
       A MagicMock of the ``version_query.Version`` object.
    :var str version:
       A string representation of the test version.
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
    """Test if `__version__` is initialized correctly.

    This test verifies whether `__version__` is correctly initialized
    as a string and checks if its value matches the result of
    `Version.from_str("0.0.1").to_str()`.

    :var str __version__: The module's version value.
    """
    with patch("k8s_agent.get_version", return_value="1.2.3"):
        from k8s_agent import __version__
        assert isinstance(__version__, str)
        assert __version__ == version_query.Version.from_str("0.0.1").to_str()
