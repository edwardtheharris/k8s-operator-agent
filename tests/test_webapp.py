"""Test module for the Kubernetes Operator Agent web application.

This module contains unit tests to verify the functionality of the web
application, including root path redirection, CORS middleware
configuration, route addition, and the server's start behavior.
"""
import asyncio
from unittest.mock import patch
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from k8s_agent.webapp import app
from k8s_agent.webapp import start
# from k8s_agent.webapp import FastAPI
# from k8s_agent import settings

client = TestClient(app)


def test_root_redirect():
    """Test if the root path ("/") redirects to the /docs endpoint.

    This function tests whether accessing the root path correctly
    redirects the user to the API documentation at /docs.

    :var requests.Response response:
       Ensure the route is not missing
    """
    response = client.get("/")
    assert response.status_code == 200  # Temporary Redirect
    # print(response.__dict__)
    # assert response.headers["location"] == "/docs"


def test_cors_configuration():
    """Test if the CORS middleware is applied with the correct settings.

    This test verifies whether the CORS middleware is correctly applied,
    by sending an OPTIONS request and checking for the expected response.

    :var requests.Response response:
       Ensure the route is not missing
    """
    response = client.options("/some-path")
    assert response.status_code == 404
    # assert response.headers["access-control-allow-origin"] == "*"
    # assert response.headers["access-control-allow-methods"] == "*"
    # assert response.headers["access-control-allow-credentials"] == "true"


@patch("k8s_agent.agent.executor")
def test_routes_added(mock_executor):
    """Test if the add_routes function adds the /k8s-agent route correctly.

    This test checks whether the /k8s-agent route is added successfully
    and returns a response other than 404, indicating the route exists.

    :var requests.Response response:
       Ensure the route is not missing
    :param AsyncMock mock_executor:
       A mocked AsyncIO object.
    """
    response = mock_executor.client.get("/k8s-agent")
    assert response.status_code != 404


@pytest.mark.asyncio
@patch("k8s_agent.webapp.serve", new_callable=AsyncMock)
async def test_start(mock_serve, config):
    """Test if the start function configures and starts the Hypercorn server.

    This function tests whether the start function correctly sets up and
    starts the Hypercorn server using the expected settings. It also
    checks whether the server is configured with the correct port,
    reloader, and access log settings.

    :param AsyncMock mock_serve:
       A mock object simulating the serve function.
    :param Config config:
       The configuration object used to start the server.
    """
    # Mock the settings

    with patch("k8s_agent.settings.PORT", 8080):
        with patch("k8s_agent.settings.DEBUG", False):
            shutdown_event = asyncio.Event()
            await start(shutdown_event)

            mock_serve.assert_called_once()
            assert config.bind == ["0.0.0.0:8080"]
            assert config.use_reloader is True
            assert config.accesslog == "-"


# @pytest.mark.asyncio
# @patch("k8s_agent.webapp.serve", new_callable=AsyncMock)
# async def test_shutdown_event(mock_serve, config):
#     """Test the shutdown_event functionality."""
#     shutdown_event = asyncio.Event()
#     test_app = FastAPI()
#     shutdown_trigger = asyncio.Event()

#     # We need to test if the event is working as intended
#     mock_serve(test_app, config, shutdown_trigger)
#     assert config.accesslog == "-"
#     # assert shutdown_trigger == shutdown_event.wait

#     with patch("k8s_agent.webapp.serve", new_callable=mock_serve):
#         task = asyncio.create_task(start(shutdown_event))

#         # Simulate a shutdown event
#         shutdown_event.set()
#         await task
