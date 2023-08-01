"""
Checks whether subscribe_example.SubscribingFeature works as expected.
"""

import asyncio
import json

import pytest
from brewblox_service import mqtt, scheduler
from brewblox_service.testing import matching

from YOUR_PACKAGE import subscribe_example
from YOUR_PACKAGE.models import ServiceConfig

TESTED = subscribe_example.__name__


@pytest.fixture
async def setup(app, mqtt_container):
    config: ServiceConfig = app['config']

    # We need to override the connection settings for the MQTT broker
    # The `mqtt_container` fixture in conftest.py started the broker on a random port
    config.mqtt_host = 'localhost'
    config.mqtt_port = mqtt_container['mqtt']

    # The subscriber depends on the `scheduler` and `mqtt` features being enabled.
    # We need to call their setup() functions during our test setup.
    scheduler.setup(app)
    mqtt.setup(app)
    subscribe_example.setup(app)


@pytest.fixture(autouse=True)
async def connected(app, client):
    # The MQTT container takes time to start
    # and the MQTT feature is not connected immediately.
    # Here, we wait until the MQTT feature is ready.
    #
    # Because the fixture is marked with `autouse=True`,
    # it will be used in all test cases in this file.
    #
    # asyncio.wait_for() raises a TimeoutError after `timeout` elapsed.
    # This prevents your tests from waiting forever if there's a bug.
    await asyncio.wait_for(mqtt.fget(app).ready.wait(), timeout=5)


async def test_on_direct_message(app, client, mocker):
    # If we want to check whether a function is called
    # without mocking its behavior, we can set a spy
    s_logger = mocker.spy(subscribe_example, 'LOGGER')

    # We directly call `on_message()` here to test functionality without
    # using the MQTT broker.
    sub = subscribe_example.fget(app)
    await sub.on_message('dummy_topic', json.dumps({'to': 'world'}))

    # The actual call:
    # LOGGER.info(f'Message on topic {topic} = {message}')
    #
    # Let's assume we're not 100% sure how info will be formatted,
    # just that it should include topic and message body.
    # The `matching` test helper lets us compare with a regex string.
    s_logger.info.assert_called_once_with(matching(r'.*dummy_topic.*to.*world.*'))


async def test_on_mqtt_message(app, client, mocker):
    # If we want to check whether a function is called
    # without mocking its behavior, we can set a spy
    s_logger = mocker.spy(subscribe_example, 'LOGGER')

    # We now test with a real MQTT message
    # We first create a new listener, so we know when the message was received
    recv_event = asyncio.Event()

    async def listener(topic: str, payload: str):
        recv_event.set()

    # There's no need to call mqtt.subscribe() - subscribe_example already did that
    await mqtt.listen(app, 'brewcast/history/#', listener)

    await mqtt.publish(app, 'brewcast/history', json.dumps({'ping': 'pong'}))

    # Wait until our own listener has received the message
    await recv_event.wait()

    s_logger.info.assert_called_once_with(matching(r'.*ping.*pong.*'))
