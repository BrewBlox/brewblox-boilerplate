"""
Checks whether we can call the hello endpoint.
"""

import pytest

from YOUR_PACKAGE import http_example


@pytest.fixture
async def app(app):
    http_example.setup(app)
    return app


async def test_hello(app, client):
    res = await client.post('/example/endpoint', data='hello')
    assert res.status == 200
    assert await res.text() == 'Hello world! (You said: "hello")'
