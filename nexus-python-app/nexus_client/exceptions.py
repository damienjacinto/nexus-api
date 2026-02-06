"""Custom exceptions for Nexus API client."""


class NexusException(Exception):
    """Base exception for all Nexus client errors."""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class NexusAuthenticationError(NexusException):
    """Raised when authentication fails."""
    pass


class NexusNotFoundError(NexusException):
    """Raised when a resource is not found (404)."""
    pass


class NexusForbiddenError(NexusException):
    """Raised when access is forbidden (403)."""
    pass


class NexusBadRequestError(NexusException):
    """Raised when the request is invalid (400)."""
    pass
