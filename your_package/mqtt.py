from contextlib import asynccontextmanager
from contextvars import ContextVar

from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

from . import utils

CV: ContextVar[FastMQTT] = ContextVar('mqtt.client')
"""
The shared MQTT client for this service.

ContextVar allows us to store a variable in a way that's both easily accessible,
and automatically cleared between tests or when hot reloading the service.
"""


def setup():
    """
    Creates the MQTT client,
    and makes it available to other modules through the `CV` ContextVar.
    """
    config = utils.get_config()
    mqtt_config = MQTTConfig(host=config.mqtt_host,
                             port=config.mqtt_port,
                             ssl=(config.mqtt_protocol == 'mqtts'),
                             reconnect_retries=-1)
    fmqtt = FastMQTT(config=mqtt_config)
    CV.set(fmqtt)


@asynccontextmanager
async def lifespan():
    """
    Handles startup and shutdown of the MQTT client.

    `setup()` must have been called first.
    This function only yields after it is connected to the MQTT eventbus.
    """
    fmqtt = CV.get()
    await fmqtt.mqtt_startup()
    yield
    await fmqtt.mqtt_shutdown()
