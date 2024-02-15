"""
Tests the HTTP example endpoints.

This includes minimal setup. We don't load what we don't need for this test.
"""

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from your_package import http_example


@pytest.fixture
def app() -> FastAPI:
    """
    We override the `app` fixture from conftest.py
    to set up the components we need for these tests.

    Now, when we use the `client` fixture, it uses this `app` fixture.
    """

    app = FastAPI()
    app.include_router(http_example.router)

    return app


async def test_endpoint(client: AsyncClient):
    # We didn't prefix the router with service name in `app.include_router()`
    # The endpoint is router prefix (/example) + endpoint address (/endpoint)
    resp = await client.post('/example/endpoint', json={'content': 'hello'})
    assert resp.status_code == 200
    assert resp.json() == {'content': 'Hi! You said `hello`.'}

    # If we send invalid data, the service immediately returns a 422 error
    resp = await client.post('/example/endpoint', json={})
    assert resp.status_code == 422
