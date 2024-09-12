"""Kubernetes Operator Agent web application module.

This module defines a FastAPI-based web application for the Kubernetes
Operator Agent. It handles HTTP requests, includes CORS middleware, and
defines routes to expose the agent's functionality.

The following imports were removed.

```{code-block} python
from fastapi.staticfiles import StaticFiles
```
"""

import asyncio

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from hypercorn.asyncio import serve
from hypercorn.config import Config
from langserve import add_routes

from . import agent, settings

#: Initialize the FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    """Handle requests for the root of the application.

    Redirect users accessing the root URL ("/") to the API documentation
    located at "/docs".
    """
    return RedirectResponse("/docs")

#: Add routes for the Kubernetes agent to handle requests at "/k8s-agent"
add_routes(
    app,
    agent.executor,
    path="/k8s-agent",
    config_keys=["metadata", "configurable", "tags"],
)


async def start(shutdown_event: asyncio.Event):
    """Start the web application.

    This function initializes and starts the FastAPI web server using
    Hypercorn. It listens on the port specified in the settings and
    remains running until the shutdown event is triggered.

    :param asyncio.Event shutdown_event:
       Event that triggers the shutdown of the web application.
    :var hypercorn.config.Config config:
       The web application configuration settings.
    """
    config = Config()
    config.bind = [f"0.0.0.0:{settings.PORT}"]
    config.use_reloader = settings.DEBUG
    config.accesslog = "-"
    return await serve(app, config, shutdown_trigger=shutdown_event.wait)
