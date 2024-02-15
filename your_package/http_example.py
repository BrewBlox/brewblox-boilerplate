"""
An example of how to register HTTP endpoints.

This is just a minimal example.
For more information, see https://fastapi.tiangolo.com/
"""

from fastapi import APIRouter

from .models import ExampleMessage

# By using APIRouter, we can declare endpoints in separate files
# We create the `FastAPI` app in app_factory.py, and then load this router
router = APIRouter(prefix='/example', tags=['Example'])


@router.post('/endpoint')
async def endpoint_post(message: ExampleMessage) -> ExampleMessage:
    """
    An example endpoint.

    The Pydantic models are automatically validated for both arguments
    and returned data.

    All endpoints are listed and can be called at {service_name}/api/doc.
    This docstring message is used as the description for this endpoint.
    """
    return ExampleMessage(content=f'Hi! You said `{message.content}`.')
