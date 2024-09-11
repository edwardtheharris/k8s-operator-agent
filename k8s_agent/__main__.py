"""Kubernetes Agent signal handling.

This script initializes a Kubernetes agent that handles termination
signals (SIGTERM, SIGINT) and ensures a graceful shutdown of the web
application. The agent runs an asyncio event loop that listens for these
signals and triggers a shutdown event when received.
"""

from typing import Any
import asyncio
import signal

from . import webapp

if __name__ == "__main__":
    #: Initialize the shutdown event that will be triggered upon receiving
    #: a signal
    shutdown_event = asyncio.Event()

    def _signal_handler(*_: Any) -> None:
        shutdown_event.set()

    loop = asyncio.get_event_loop_policy().get_event_loop()

    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    loop.add_signal_handler(signal.SIGINT, _signal_handler)

    loop.run_until_complete(asyncio.gather(webapp.start(shutdown_event)))
