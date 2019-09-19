"""
Example on how to listen to RabbitMQ events.

For an example on how to publish events, see poll_example.py
"""

from typing import Union

from aiohttp import web
from brewblox_service import brewblox_logger, events

LOGGER = brewblox_logger(__name__)


async def on_message(subscription: events.EventSubscription, key: str, message: Union[dict, str]):
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


def setup(app: web.Application):
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

    # Get the standard event listener
    # This can be used to register as many subscriptions as you want
    listener = events.get_listener(app)

    # Subscribe to all events on 'brewblox' exchange
    listener.subscribe('brewblox', '#', on_message=on_message)
