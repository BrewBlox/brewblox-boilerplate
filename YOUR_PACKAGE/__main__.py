"""
Example of how to import and use the brewblox service
"""

import logging
from typing import Type

from aiohttp import web

from brewblox_service import events, service

routes = web.RouteTableDef()
LOGGER = logging.getLogger(__name__)


@routes.get('/hello')
async def greet(request: Type[web.Request]):
    return web.Response(body='Hello world!')


async def on_message(queue, key, message):
    LOGGER.info(f'Message from {queue}: {key} = {message} ({type(message)})')


def main():
    app = service.create()

    # Add event handling
    events.setup(app)
    listener = events.get_listener(app)
    listener.subscribe('brewblox', '#', on_message=on_message)

    # Register own routes
    app.router.add_routes(routes)

    # Add all default endpoints, and announce service to gateway
    service.furnish(app)

    # service.run() will start serving clients async
    service.run(app)


if __name__ == '__main__':
    main()
