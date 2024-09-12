"""Kubernetes Operator Agent settings unit tests module."""
import os
import pytest

# Import the settings module from k8s_agent
from k8s_agent import settings
from k8s_agent.settings import DEBUG
from k8s_agent.settings import LOG_LEVEL
from k8s_agent.settings import OLLAMA_BASE_URL
from k8s_agent.settings import OLLAMA_MODEL
from k8s_agent.settings import OPENAI_MODEL
from k8s_agent.settings import OPENAI_MODEL_TEMP
from k8s_agent.settings import PORT
from k8s_agent.settings import REDIS_URL

def test_langchain_endpoint():
    """
    Test that `LANGCHAIN_ENDPOINT` is set to the correct default value.
    """
    assert os.environ.get("LANGCHAIN_ENDPOINT") == \
        "https://api.smith.langchain.com"

def test_langchain_project():
    """
    Test that `LANGCHAIN_PROJECT` is set to the correct default value.
    """
    assert os.environ.get("LANGCHAIN_PROJECT") == "k8s-agent"

def test_debug_setting():
    """
    Test that DEBUG is set to True by default and is of type bool.

    :var bool DEBUG:
       Enable or disable debug output.
    """
    assert isinstance(DEBUG, bool)
    assert DEBUG is True

def test_log_level_debug():
    """
    Test that LOG_LEVEL is set to DEBUG when DEBUG is True.

    :var str LOG_LEVEL:
       Setting to determine the verbosity of log output.
    """
    assert LOG_LEVEL == "DEBUG"

def test_ollama_base_url():
    """
    Test that OLLAMA_BASE_URL is set to the default value.

    :var str OLLAMA_BASE_URL:
      URL for an Open LLAMA server to use.
    """
    assert OLLAMA_BASE_URL == "http://localhost:11434"

def test_ollama_model():
    """
    Test that OLLAMA_MODEL is set to the default value.

    :var str OLLAMA_MODEL:
       The OLLAMA model to be used.
    """
    assert OLLAMA_MODEL == "http://localhost:11434"

def test_openai_model():
    """
    Test that OPENAI_MODEL is set to the default value.

    :var str OPENAI_MODEL:
       Name of the OpenAI model to use.
    """
    assert OPENAI_MODEL == "gpt-4-0125-preview"

def test_openai_model_temp():
    """
    Test that OPENAI_MODEL_TEMP is set to the correct default value.

    :var str OPENAI_MODEL_TEMP:
       Value of OpenAI Model temp setting.
    """
    assert isinstance(OPENAI_MODEL_TEMP, float)
    assert OPENAI_MODEL_TEMP == 0.0

def test_port():
    """
    Test that PORT is set to the correct default value of 8000.

    :var str PORT:
       The port that the agent will listen on.
    """
    assert isinstance(PORT, int)
    assert PORT == 8000

def test_redis_url():
    """
    Test that REDIS_URL is set to the default Redis server URL.

    :var str REDIS_URL:
      URL for a working Redis server.
    """
    assert REDIS_URL == "redis://localhost:6379/0"

@pytest.mark.parametrize(
    "env_var,default_value,var_type",
    [
        ("PORT", 8000, int),
        ("OPENAI_MODEL_TEMP", 0.0, float),
        ("OLLAMA_BASE_URL", "http://localhost:11434", str),
        ("LOG_LEVEL", "DEBUG", str),
    ]
)
def test_defaults(env_var, default_value, var_type):
    """
    Parameterized test to check various environment variable default values.

    :param str env_var: The environment variable under test.
    :param str default_value: The expected default value.
    :param str var_type: The type of the expected value.
    """
    env_value = getattr(settings, env_var)
    assert isinstance(env_value, var_type)
    assert env_value == default_value
