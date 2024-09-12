"""Pytest configuration module.

This module sets up configurations and fixtures for Pytest, allowing
the test environment to include custom configurations for the application.
"""

from pathlib import Path
import sys

from hypercorn.config import Config

import pytest

#: Add the parent directory of the current file to the system path
MODULE_DIR = str(Path(__file__).parent.parent.resolve())
sys.path.append(MODULE_DIR)


@pytest.fixture
def config():
    """Provide a Hypercorn Config object for testing.

    This fixture returns a pre-configured Hypercorn
    ``hypercorn.config.Config`` object
    used for testing purposes. It binds the server to `0.0.0.0:8080`,
    enables the reloader, and sets the access log to stdout.

    :var hypercorn.config.Config ret_value: The HyperCorn Config object.
    :return ret_value:
        The configured Hypercorn ``Config`` object.
    """
    ret_value = Config()
    ret_value.bind = ["0.0.0.0:8080"]
    ret_value.use_reloader = True
    ret_value.accesslog = "-"
    return ret_value
