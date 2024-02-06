"""Pytest configuration module."""

from pathlib import Path
import sys

from hypercorn.config import Config

import pytest

MODULE_DIR = str(Path(__file__).parent.parent.resolve())
sys.path.append(MODULE_DIR)


@pytest.fixture
def config():
    """Return a config object."""
    ret_value = Config()
    ret_value.bind = ["0.0.0.0:8080"]
    ret_value.use_reloader = True
    ret_value.accesslog = "-"
    return ret_value
