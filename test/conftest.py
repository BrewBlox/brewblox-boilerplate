"""
Master file for pytest fixtures.
Any fixtures declared here are available to all test functions in this directory.
"""


import logging
from typing import AsyncGenerator, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from your_package import app_factory, utils
from your_package.models import ServiceConfig

LOGGER = logging.getLogger(__name__)


class TestConfig(ServiceConfig):
    """
    An override for ServiceConfig that only uses
    settings provided to __init__()

    This makes tests independent of env values.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings,)


@pytest.fixture(autouse=True)
def config(monkeypatch: pytest.MonkeyPatch) -> Generator[ServiceConfig, None, None]:
    """
    Replaces `utils.get_config()` with a function that returns TestConfig.
    """
    cfg = TestConfig(
        debug=True,
    )
    monkeypatch.setattr(utils, 'get_config', lambda: cfg)
    yield cfg


@pytest.fixture(autouse=True)
def setup_logging(config):
    """
    Initializes logging.
    Logger output will be shown for failing tests.
    """
    app_factory.setup_logging(True)


@pytest.fixture
def app() -> FastAPI:
    """
    Override this in test modules to bootstrap required dependencies.

    IMPORTANT: This must NOT be an async fixture.
    Contextvars assigned in async fixtures are invisible to test functions.
    """
    app = FastAPI()
    return app


@pytest.fixture
async def manager(app: FastAPI) -> AsyncGenerator[LifespanManager, None]:
    """
    AsyncClient does not automatically send ASGI lifespan events to the app
    https://asgi.readthedocs.io/en/latest/specs/lifespan.html

    For testing, this ensures that lifespan() functions are handled.
    If you don't need to make HTTP requests, you can use `manager`
    without the `client` fixture.
    """
    async with LifespanManager(app) as mgr:
        yield mgr


@pytest.fixture
async def client(app: FastAPI, manager: LifespanManager) -> AsyncGenerator[AsyncClient, None]:
    """
    The default test client for making REST API calls.
    Using this fixture will also guarantee that lifespan startup has happened.
    """
    # AsyncClient does not automatically send ASGI lifespan events to the app
    # https://asgi.readthedocs.io/en/latest/specs/lifespan.html
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
