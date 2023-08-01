"""
Master file for pytest fixtures.
Any fixtures declared here are available to all test functions in this directory.
"""


import logging

import pytest
from aiohttp import test_utils
from brewblox_service import brewblox_logger, features, service, testing

from YOUR_PACKAGE.models import ServiceConfig

LOGGER = brewblox_logger(__name__)


@pytest.fixture(scope='session', autouse=True)
def log_enabled():
    """Sets log level to DEBUG for all test functions.
    Allows all logged messages to be captured during pytest runs"""
    logging.getLogger().setLevel(logging.DEBUG)
    logging.captureWarnings(True)


@pytest.fixture
def app_config() -> ServiceConfig:
    return ServiceConfig(
        # From brewblox_service
        name='test_app',
        host='localhost',
        port=1234,
        debug=True,
        mqtt_protocol='mqtt',
        mqtt_host='eventbus',
        mqtt_port=1883,
        mqtt_path='/eventbus',
        history_topic='brewcast/history',
        state_topic='brewcast/state',

        # From this service
        poll_interval=5,
    )


@pytest.fixture
def sys_args(app_config: ServiceConfig) -> list:
    return [str(v) for v in [
        'app_name',
        '--name', app_config.name,
        '--poll-interval', app_config.poll_interval,
        '--debug',
    ]]


@pytest.fixture
def app(app_config):
    app = service.create_app(app_config)
    return app


@pytest.fixture
async def setup(app):
    """
    This fixture is defined here so it can be overriden later.
    If you wish to call setup() for various features at the start of your tests,
    you can override this fixture, and use it to do so.
    """


@pytest.fixture
async def client(app, setup, aiohttp_client, aiohttp_server):
    LOGGER.debug('Available features:')
    for name, impl in app.get(features.FEATURES_KEY, {}).items():
        LOGGER.debug(f'Feature "{name}" = {impl}')
    LOGGER.debug(app.on_startup)

    test_server: test_utils.TestServer = await aiohttp_server(app)
    test_client: test_utils.TestClient = await aiohttp_client(test_server)
    return test_client


@pytest.fixture(scope='session')
def mqtt_container():
    with testing.docker_container(
        name='mqtt-test-container',
        ports={'mqtt': 1883},
        args=['ghcr.io/brewblox/mosquitto:develop'],
    ) as ports:
        yield ports
