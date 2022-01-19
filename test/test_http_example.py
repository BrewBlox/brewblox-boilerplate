"""
Checks whether we can call the hello endpoint.
"""

import pytest
from brewblox_service.testing import response

from YOUR_PACKAGE import http_example


@pytest.fixture
def app(app):
    """
    This overrides the fixture defined in conftest.py.
    We can depend on the original fixture and modify its result.
    All other tests and fixtures that depend on `app` will use the modified result.
    """
    http_example.setup(app)
    return app


async def test_hello(app, client):
    """
    This test depends on a running application.
    We depend on the `app` fixture to get an application where `http_example.setup(app)`
    has been called.
    We depend on the `client` fixture where the app was started,
    and is now listening for HTTP requests.
    """
    # Basic call to the GET handler
    res = await client.get('/example/endpoint')
    assert res.status == 200
    assert (await res.json()) == {'content': 'Hello world!'}

    # The `response()` test helper automatically checks the status code, and calls res.json()
    assert await response(
        client.get('/example/endpoint')
    ) == {'content': 'Hello world!'}

    # Call the POST handler
    assert await response(
        client.post('/example/endpoint', json={'content': 'hello'})
    ) == {'content': 'Hi! You said `hello`.'}

    # The response handler can also check for non-200 responses
    # For example, if we send the wrong arguments
    assert await response(
        client.post('/example/endpoint', json={'content': ['hello', 'world']}),
        status=400
    ) == [{
        'loc': ['content'],
        'msg': 'str type expected',
        'type': 'type_error.str',
        'in': 'body',
    }]
