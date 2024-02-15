"""
An example of how to subscribe to MQTT events.

MQTT is a publish/subscribe message protocol.
In Brewblox it's commonly used to publish history data and service state.

For an explanation on MQTT, see https://randomnerdtutorials.com/what-is-mqtt-and-how-it-works/

For reference documentation on MQTT in Brewblox, see https://www.brewblox.com/dev/

For this example, we'll listen in on Brewblox history messages.
"""

import json
import logging

from . import mqtt, utils

LOGGER = logging.getLogger(__name__)


def setup():
    config = utils.get_config()
    mqtt_client = mqtt.CV.get()  # `mqtt.CV` is set in `mqtt.setup()`

    # Set a callback for when the eventbus receives a message that matches this topic
    # Subscriptions must be set before the MQTT client is connected
    @mqtt_client.subscribe(config.history_topic + '/#')
    async def on_history_message(client, topic, payload, qos, properties):
        evt = json.loads(payload)
        key = evt['key']
        data = evt['data']
        LOGGER.info(f'{topic=}, {key=}')
        LOGGER.debug(f'{key=}, {data=}')
