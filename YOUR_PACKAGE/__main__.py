"""
Example of how to import and use the brewblox service
"""

import logging
from typing import Type

from aiohttp import web

from brewblox_service import events, service

routes = web.RouteTableDef()
LOGGER = logging.getLogger(__name__)


@routes.post('/example/endpoint')
async def example_endpoint_handler(request: Type[web.Request]):
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


async def on_message(subscription, key, message):
    """Example message handler for RabbitMQ events.

    Services can choose to publish / subscribe events to communicate between them.
    These events are for loose communication: you broadcast something,
    and don't really care by whom it gets picked up.

    When subscribing to an event, you provide a callback (example: this function)
    that will be called every time a relevant event is published.

    Args:
        subscription (events.EventSubscription):
            The subscription that triggered this callback.

        key (str): The routing key of the published event.
            This will always be specific - no wildcards.

        message (dict | str): The content of the event.
            If it was a JSON message, this is a dict. String otherwise.

    """
    LOGGER.info(f'Message from {subscription}: {key} = {message} ({type(message)})')


def add_events(app):
    """Add event handling

    Subscriptions can be made at any time using `EventListener.subscribe()`.
    They will be declared on the remote amqp server whenever the listener is connected.

    Message interest can be specified by setting exchange name, and routing key.

    For `direct` and `fanout` exchanges, messages must match routing key exactly.
    For `topic` exchanges (the default), routing keys can be multiple values, separated with dots (.).
    Routing keys can use regex and wildcards.

    The simple wildcards are `*` and `#`.

    `*` matches a single level.

    "controller.*.sensor" subscriptions will receive (example) routing keys:
    - controller.block.sensor
    - controller.container.sensor

    But not:
    - controller
    - controller.nested.block.sensor
    - controller.block.sensor.nested

    `#` is a greedier wildcard: it will match as few or as many values as it can
    Plain # subscriptions will receive all messages published to that exchange.

    A subscription of "controller.#" will receive:
    - controller
    - controller.block.sensor
    - controller.container.nested.sensor

    For more information on this, see https://www.rabbitmq.com/tutorials/tutorial-four-python.html
    and https://www.rabbitmq.com/tutorials/tutorial-five-python.html
    """

    # Enable event handling
    # Event subscription / publishing will be enabled after you call this function
    events.setup(app)

    # Get the standard event listener
    # This can be used to register as many subscriptions as you want
    listener = events.get_listener(app)

    # Subscribe to all events on 'brewblox' exchange
    listener.subscribe('brewblox', '#', on_message=on_message)


def main():
    app = service.create_app(default_name='YOUR_PACKAGE')

    add_events(app)

    # Register routes in this file (/example/endpoint in our case)
    app.router.add_routes(routes)

    # Add all default endpoints, and adds prefix to all endpoints
    #
    # Default endpoints are:
    # {prefix}/api/doc (Swagger documentation of endpoints)
    # {prefix}/_service/status (Health check: this endpoint is called to check service status)
    #
    # The prefix is automatically added for all endpoints. You don't have to do anything for this.
    # To change the prefix, you can use the --name command line argument.
    #
    # See brewblox_service.service for more details on how arguments are parsed.
    #
    # The default value is "YOUR_PACKAGE" (provided in service.create_app()).
    # This means you can now access the example/endpoint as "/YOUR_PACKAGE/example/endpoint"
    service.furnish(app)

    # service.run() will start serving clients async
    service.run(app)


if __name__ == '__main__':
    main()
