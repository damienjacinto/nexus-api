"""
Nexus Repository Manager REST API Client for Python

This package provides a comprehensive Python client for interacting with
Sonatype Nexus Repository Manager REST API.
"""

from .client import NexusClient
from .exceptions import NexusException, NexusAuthenticationError, NexusNotFoundError

__version__ = "1.0.0"
__all__ = ["NexusClient", "NexusException", "NexusAuthenticationError", "NexusNotFoundError"]
