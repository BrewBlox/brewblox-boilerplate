import logging
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from . import (http_example, mqtt, mqtt_publish_example,
               mqtt_subscribe_example, utils)

LOGGER = logging.getLogger(__name__)


def setup_logging(debug: bool):
    """
    Initializes logging, defining log level and formatting.
    """
    # 2024/02/15 14:48:05.963 [I:your_package.app_factory:16] example message
    format = '%(asctime)s.%(msecs)03d [%(levelname).1s:%(name)s:%(lineno)d] %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(level=level, format=format, datefmt=datefmt)
    logging.captureWarnings(True)

    # You can edit log levels for library modules here
    # This helps with log spam
    logging.getLogger('gmqtt').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.error').disabled = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    The application lifespan: startup and shutdown events.

    With this, we can control background tasks and shared clients.
    The lifespan context exits just before the service shuts down.

    https://fastapi.tiangolo.com/advanced/events/
    """
    LOGGER.info(utils.get_config())

    # With an AsyncExitStack, we can combine multiple context managers
    # without having to increase indentation
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(mqtt.lifespan())
        await stack.enter_async_context(mqtt_publish_example.lifespan())
        yield


def create_app() -> FastAPI:
    """
    The application factory.

    This method is called by uvicorn to start the service.
    Uvicorn is started in `entrypoint.sh`.
    """
    config = utils.get_config()
    setup_logging(config.debug)

    # Call setup functions for modules
    mqtt.setup()
    mqtt_subscribe_example.setup()

    # Create app
    # OpenApi endpoints are set to /api/doc for backwards compatibility
    prefix = f'/{config.name}'
    app = FastAPI(lifespan=lifespan,
                  docs_url=f'{prefix}/api/doc',
                  redoc_url=f'{prefix}/api/redoc',
                  openapi_url=f'{prefix}/openapi.json')

    # Include all endpoints declared by modules
    app.include_router(http_example.router, prefix=prefix)

    return app
