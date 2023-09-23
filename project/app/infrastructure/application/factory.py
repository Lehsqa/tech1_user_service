import asyncio
from functools import partial
from typing import Callable, Coroutine, Iterable

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


def create(
    *_,
    rest_routers: Iterable[APIRouter],
    startup_tasks: Iterable[Callable[[], Coroutine]] or None = None,
    shutdown_tasks: Iterable[Callable[[], Coroutine]] or None = None,
    **kwargs,
) -> FastAPI:

    # Initialize the base FastAPI application
    app = FastAPI(**kwargs)

    # Include REST API routers
    for router in rest_routers:
        app.include_router(router)

    # Define startup tasks that are running asynchronous using FastAPI hook
    if startup_tasks:
        for task in startup_tasks:
            coro = partial(asyncio.create_task, task())
            app.on_event("startup")(coro)

    # Define shutdown tasks using FastAPI hook
    if shutdown_tasks:
        for task in shutdown_tasks:
            app.on_event("shutdown")(task)

    return app
