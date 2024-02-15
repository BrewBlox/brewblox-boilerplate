"""
Tests the MQTT publishing example tests.

This includes minimal setup, and mocking of the actual MQTT client.
"""


import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from datetime import timedelta
from unittest.mock import ANY, Mock

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi_mqtt import MQTTClient

from your_package import mqtt, mqtt_publish_example, utils


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    We replicate `lifespan()` from `app_factory.py` here,
    but only with what we need for this test
    """
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(mqtt_publish_example.lifespan())
        yield


@pytest.fixture
def app() -> FastAPI:
    """
    We override the `app` fixture from conftest.py
    to set up the components we need for these tests.

    Now, when we use the `manager` fixture, it uses this `app` fixture.
    """
    # We don't want to wait multiple seconds when testing
    # Override the setting so we don't have to
    config = utils.get_config()
    config.publish_interval = timedelta(milliseconds=10)

    # We create a Mock object that replicates the functions of `MQTTClient`
    # We set the ContextVar in `mqtt.py` with this mock,
    # so it gets used by `mqtt_publish_example.py`
    # This replaces `mqtt.setup()`
    mqtt.CV.set(Mock(spec=MQTTClient))

    app = FastAPI(lifespan=lifespan)
    return app


async def test_publish(manager: LifespanManager):
    # We want the app lifespan() to start, but we don't need to send HTTP requests
    # For this test, we can use the `manager` fixture from conftest.

    # In the `app` fixture, we placed a Mock object in `mqtt.CV`
    m_mqtt_client: Mock = mqtt.CV.get()

    # Let the publisher do it's thing for a bit
    await asyncio.sleep(0.1)

    # We expect the publish call to have been used
    assert m_mqtt_client.publish.call_count > 0

    # The topic is `f'{config.history_topic}/{config.name}'`
    # In tests, that equals `brewcast/history/your_package`
    # The value is random, so we just match it with `ANY`
    assert m_mqtt_client.publish.call_args_list[0].args == ('brewcast/history/your_package',
                                                            {'key': 'your_package',
                                                             'data': {'value[degC]': ANY}})
