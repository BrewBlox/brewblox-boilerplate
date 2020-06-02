"""
Example on how to listen to MQTT events.

For an example on how to publish events, see poll_example.py
"""


from aiohttp import web
from brewblox_service import brewblox_logger, mqtt

LOGGER = brewblox_logger(__name__)


async def on_message(topic: str, message: dict):
    """Example message handler for MQTT events.

    Services can choose to publish / subscribe events to communicate between them.
    These events are for loose communication: you broadcast something,
    and don't really care by whom it gets picked up.

    When subscribing to an event, you provide a callback (example: this function)
    that will be called every time a relevant event is published.

    Args:
        subscription (events.EventSubscription):
            The subscription that triggered this callback.

        topic (str):
            The topic to which this event was published.
            This will always be specific - no wildcards.

        message (dict):
            The content of the event.
            Messages handled by mqtt.py are always parsed to JSON.

    """
    LOGGER.info(f'Message on topic {topic} = {message}')


def setup(app: web.Application):
    """Add event handling

    To get messages, you need to call `mqtt.subscribe(topic)` and `mqtt.listen(topic, callback)`.

    You can set multiple listeners for each call to subscribe, and use wildcards to filter messages.

    Wildcards are + or #

    + matches a single level.

    "controller/+/sensor" subscriptions will receive (example) topics:
    - controller/block/sensor
    - controller/container/sensor

    But not:
    - controller
    - controller/nested/block/sensor
    - controller/block/sensor/nested

    # is a greedier wildcard: it will match as few or as many values as it can
    Plain # subscriptions will receive all messages published to the eventbus.

    A subscription of "controller/#" will receive:
    - controller
    - controller/block/sensor
    - controller/container/nested/sensor

    For more information on this, see
    http://www.steves-internet-guide.com/understanding-mqtt-topics/
    """

    mqtt.listen(app, 'brewcast/history/#', on_message)
    mqtt.subscribe(app, 'brewcast/history/#')
