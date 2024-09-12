"""Kubernetes Operator Agent configuration settings.

This module defines environment variables and configuration settings
for the Kubernetes Operator Agent, including API endpoints, model
settings, debugging options, and external services.
"""
import os

#: Set the LangChain API endpoint and project name in the environment
os.environ.update({"LANGCHAIN_ENDPOINT": "https://api.smith.langchain.com"})
os.environ.update({"LANGCHAIN_PROJECT": "k8s-agent"})

#: Debugging mode is set via the DEBUG environment variable, defaults to True
DEBUG = bool(os.environ.get("DEBUG", True))
#: Log level is set based on DEBUG status, defaults to "DEBUG" or "WARNING"
LOG_LEVEL = os.environ.get("LOG_LEVEL", DEBUG and "DEBUG" or "WARNING")
#: Base URL for the Ollama model server, defaults to localhost
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
#: Ollama model configuration, defaults to a local server
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "http://localhost:11434")
#: OpenAI model configuration, defaults to a specific GPT-4 model version
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4-0125-preview")
#: OpenAI model temperature setting, controls response randomness.
#:
#: Defaults to 0 (deterministic responses)
OPENAI_MODEL_TEMP = float(os.environ.get("OPENAI_MODEL_TEMP", 0))
#: Port for running the agent, defaults to 8000
PORT = int(os.environ.get("PORT", 8000))
#: Redis URL for caching and task queuing, defaults to a local Redis server
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
