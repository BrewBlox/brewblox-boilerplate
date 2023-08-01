"""
Checks whether the publish_example.PublishingFeature works as expected.
"""

import asyncio
import json

import pytest
from aresponses import ResponsesMockServer
from brewblox_service import http, mqtt, repeater, scheduler

from YOUR_PACKAGE import publish_example
from YOUR_PACKAGE.models import ServiceConfig

TESTED = publish_example.__name__


@pytest.fixture(autouse=True)
def s_publish(mocker):
    """
    In conftest.py, we added the `mqtt_container` fixture.
    This starts a real MQTT broker that can receive published events.
    We still want to check that the correct data was sent.
    Here we create a spy: the function works as normal,
    but also tracks its calls.
    """
    m = mocker.spy(mqtt, 'publish')
    return m


@pytest.fixture
async def setup(app, mqtt_container):
    config: ServiceConfig = app['config']

    # We need to override the connection settings for the MQTT broker
    # The `mqtt_container` fixture in conftest.py started the broker on a random port
    config.mqtt_host = 'localhost'
    config.mqtt_port = mqtt_container['mqtt']

    # RepeaterFeature depends on the `scheduler`, `mqtt`, and `http` features being enabled.
    # We need to call their setup() functions during our test setup.
    scheduler.setup(app)
    mqtt.setup(app)
    http.setup(app)

    # We want to use the publishing feature,
    # but we don't want it to start and run automatically
    # This can be done by setting `autostart=False`
    # We now need to call `prepare()` and `run()` manually
    publish_example.setup(app, autostart=False)


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


async def test_startup(app, client):
    pub = publish_example.fget(app)

    assert isinstance(pub, publish_example.PublishingFeature)

    # the `active` property is provided by RepeaterFeature
    # It's not True yet, because we set `autostart=False`
    assert not pub.active

    # We start the feature. This will call prepare() and then run().
    await pub.start()
    assert pub.active


async def test_prepare(app, client):
    pub = publish_example.fget(app)

    # The background task is not running
    assert not pub.active

    # Manually call prepare()
    # Usually this is done in the background task
    await pub.prepare()

    # Still not active - prepare() does not start the background task
    assert not pub.active

    # Local configuration is set during prepare()
    assert pub.topic == 'brewcast/history'


async def test_prepare_cancel(app, client):
    pub = publish_example.fget(app)

    # app['config'] is set by parsing command-line arguments
    # but the result can be modified in tests
    # Here we want our background task to stop if poll interval <= 0
    # This is done by raising a specific exception (RepeaterCancelled)
    with pytest.raises(repeater.RepeaterCancelled):
        app['config'].poll_interval = 0
        await pub.prepare()


async def test_run(app, client, s_publish, aresponses: ResponsesMockServer):
    pub = publish_example.fget(app)
    config: ServiceConfig = app['config']
    # We don't want to wait the actual poll interval during tests
    config.poll_interval = 0.0001

    # We mock this specific URL
    # This tests our code in more detail than setting a generic mock on `session.get()`
    # It also makes it easier to test functions that make multiple HTTP requests.
    aresponses.add(
        host_pattern='jsonplaceholder.typicode.com',
        path_pattern='/todos/1',
        method_pattern='GET',
        response={'hello': 'world'},
    )

    await pub.prepare()
    await pub.run()

    # We mocked the response to the HTTP request,
    # and we spied on the `mqtt.publish()` function.
    # We expect publish() to be called with the mock data.
    s_publish.assert_awaited_once_with(
        app,
        config.history_topic,
        json.dumps({
            'key': config.name,
            'data': {'hello': 'world'},
        }),
    )

    # ... and we expect the mocked requests to have been used
    aresponses.assert_plan_strictly_followed()
