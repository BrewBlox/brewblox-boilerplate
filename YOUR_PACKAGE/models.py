"""
Pydantic models are declared here, and then imported wherever needed
"""

from brewblox_service.models import BaseServiceConfig


class ServiceConfig(BaseServiceConfig):
    """
    This model extends the default configuration from brewblox-service,
    and adds the arguments that were added to the parser in __main__.py
    """
    poll_interval: float
