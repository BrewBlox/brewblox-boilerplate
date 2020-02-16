"""
Example of how to import and use the brewblox service
"""

from argparse import ArgumentParser

from brewblox_service import brewblox_logger, events, http, scheduler, service
from YOUR_PACKAGE import events_example, http_example, poll_example

LOGGER = brewblox_logger(__name__)


def create_parser(default_name='YOUR_PACKAGE') -> ArgumentParser:
    # brewblox-service has some default arguments
    # We can add more arguments here before sending the parser back to brewblox-service
    # The parsed values for all arguments are placed in app['config']
    # For documentation see https://docs.python.org/3/library/argparse.html
    parser: ArgumentParser = service.create_parser(default_name=default_name)

    # This argument will be used by poll_example
    # After the service started, you can get the value in
    # app['config']['history_exchange']
    parser.add_argument('--history-exchange',
                        help='RabbitMQ eventbus exchange. [%(default)s]',
                        default='brewcast.history')

    # This will also be used by poll_example
    # Note how we specify the type as float
    parser.add_argument('--poll-interval',
                        help='Interval (in seconds) between polling. [%(default)s]',
                        type=float,
                        default=5)

    return parser


def main():

    app = service.create_app(parser=create_parser())

    # Enable the task scheduler
    # This is required for the `events` feature,
    # and for the RepeaterFeature used in poll_example
    scheduler.setup(app)

    # Enable event handling
    # Event subscription / publishing will be enabled after you call this function
    events.setup(app)

    # Enable making HTTP requests
    # This allows you to access a shared aiohttp ClientSession
    # https://docs.aiohttp.org/en/stable/client_reference.html
    http.setup(app)

    # To keep everything consistent, examples also have the setup() function
    # In here they register everything that must be done before the service starts
    # It's not required to use this pattern, but it makes code easier to understand
    events_example.setup(app)
    poll_example.setup(app)
    http_example.setup(app)

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
