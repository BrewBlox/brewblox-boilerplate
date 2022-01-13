"""
An example of how to register HTTP endpoints
"""

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200
from pydantic import BaseModel

routes = web.RouteTableDef()


def setup(app: web.Application):
    # Register routes in this file (/example/endpoint in our case)
    app.router.add_routes(routes)


class EndpointMessage(BaseModel):
    """
    For more options, see https://pydantic-docs.helpmanual.io/
    """
    content: str


@routes.view('/example/endpoint')
class ExampleEndpoint(PydanticView):
    """
    When using the PydanticView, the endpoint is automatically added to the /api/doc page.
    For more information, see: <br>
    - https://docs.aiohttp.org/en/stable/web_quickstart.html#class-based-views <br>
    - https://github.com/Maillol/aiohttp-pydantic <br>
    """

    async def get(self) -> r200[EndpointMessage]:
        """
        Example endpoint handler for GET requests.
        The docstring message will be automatically added to the /api/doc page.

        The `r200[EndpointMessage]` indicates that if everything goes ok (status 200),
        the response body contains an EndpointMessage.

        Tags: Example, Endpoint
        """
        return web.json_response(
            EndpointMessage(content='Hello world!').dict()
        )

    async def post(self, message: EndpointMessage) -> r200[EndpointMessage]:
        """
        Example endpoint handler for POST requests.
        The docstring message will be automatically added to the /api/doc page.

        When using PydanticView, you can add arguments to post / put / patch functions.
        The JSON in the request body will be automatically parsed and validated.

        Tags: Example, Endpoint
        """
        return web.json_response(
            EndpointMessage(content=f'Hi! You said `{message.content}`.').dict()
        )
