"""
An example of how to register HTTP endpoints
"""

from aiohttp import web

routes = web.RouteTableDef()


def setup(app: web.Application):
    # Register routes in this file (/example/endpoint in our case)
    app.router.add_routes(routes)


@routes.post('/example/endpoint')
async def example_endpoint_handler(request: web.Request) -> web.Response:
    """
    Example endpoint handler. Using `routes.post` means it will only respond to POST requests.

    When trying it out, it will echo whatever you send.

    Each aiohttp endpoint should take a request as argument, and return a response.
    You can add Swagger documentation in this docstring, or by adding a yaml file.
    See http://aiohttp-swagger.readthedocs.io/en/latest/ for more details

    ---
    tags:
    - Example
    summary: Example endpoint.
    description: An example of how to use aiohttp features.
    operationId: example.endpoint
    produces:
    - text/plain
    parameters:
    -
        in: body
        name: body
        description: Input message
        required: false
        schema:
            type: string
    """
    input = await request.text()
    return web.Response(body=f'Hello world! (You said: "{input}")')
