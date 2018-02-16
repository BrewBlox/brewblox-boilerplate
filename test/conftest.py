"""
Master file for pytest fixtures.
Any fixtures declared here are available to all test functions in this directory.
"""

import json
import logging

import pytest
from brewblox_service import rest
from setuptools import find_packages


@pytest.fixture(scope='session', autouse=True)
def log_enabled():
    """Sets log level to DEBUG for all test functions.
    Allows all logged messages to be captured during pytest runs"""
    logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture
def app_config() -> dict:
    return {
        'name': 'test_app',
        'service_name': find_packages(exclude=['test'])[0],
        'prefix': '',
        'plugin_dir': 'plugins',
        'port': 1234,
        'gateway': 'http://gatewayaddr:1234',
    }


@pytest.fixture
def app(app_config):
    app = rest.create_app(app_config)
    # For the plugin mechanism, we need a valid app name
    app.name = app_config['service_name']
    return app


@pytest.yield_fixture
def client(client):
    """Monkeypatch the Pytest-flask client to allow simple json post calls"""

    def jsonpost(*args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return client._post(*args, **kwargs)

    client._post = client.post
    client.post = jsonpost
    yield client
