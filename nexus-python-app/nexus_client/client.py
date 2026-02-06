"""Main Nexus Repository Manager client."""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
import logging

from .exceptions import (
    NexusException,
    NexusAuthenticationError,
    NexusNotFoundError,
    NexusForbiddenError,
    NexusBadRequestError
)
from .repositories import RepositoryAPI
from .components import ComponentAPI
from .assets import AssetAPI
from .security import SecurityAPI
from .tasks import TaskAPI
from .search import SearchAPI
from .blob_stores import BlobStoreAPI


logger = logging.getLogger(__name__)


class NexusClient:
    """
    Main client for interacting with Nexus Repository Manager REST API.

    Example:
        >>> client = NexusClient("https://nexus.example.com", username="admin", password="admin123")
        >>> repos = client.repositories.list()
        >>> components = client.components.search(repository="maven-releases")
    """

    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialize Nexus client.

        Args:
            base_url: Base URL of Nexus server (e.g., "https://nexus.example.com")
            username: Username for authentication
            password: Password for authentication
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = urljoin(self.base_url, '/service/rest/')
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.timeout = timeout

        # Session for connection pooling
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)

        # Initialize API modules
        self.repositories = RepositoryAPI(self)
        self.components = ComponentAPI(self)
        self.assets = AssetAPI(self)
        self.security = SecurityAPI(self)
        self.tasks = TaskAPI(self)
        self.search = SearchAPI(self)
        self.blob_stores = BlobStoreAPI(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Any = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request to the Nexus API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (relative to api_base)
            params: Query parameters
            json: JSON body data
            data: Raw body data
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object

        Raises:
            NexusAuthenticationError: If authentication fails
            NexusNotFoundError: If resource not found
            NexusForbiddenError: If access forbidden
            NexusBadRequestError: If request is invalid
            NexusException: For other errors
        """
        url = urljoin(self.api_base, endpoint.lstrip('/'))

        request_headers = headers or {}

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                headers=request_headers,
                verify=self.verify_ssl,
                timeout=self.timeout,
                **kwargs
            )

            # Handle different error status codes
            if response.status_code == 401:
                raise NexusAuthenticationError(
                    "Authentication failed",
                    status_code=401,
                    response=response
                )
            elif response.status_code == 403:
                raise NexusForbiddenError(
                    "Access forbidden - insufficient permissions",
                    status_code=403,
                    response=response
                )
            elif response.status_code == 404:
                raise NexusNotFoundError(
                    "Resource not found",
                    status_code=404,
                    response=response
                )
            elif response.status_code == 400:
                raise NexusBadRequestError(
                    f"Bad request: {response.text}",
                    status_code=400,
                    response=response
                )
            elif response.status_code >= 400:
                raise NexusException(
                    f"Request failed with status {response.status_code}: {response.text}",
                    status_code=response.status_code,
                    response=response
                )

            return response

        except requests.exceptions.RequestException as e:
            raise NexusException(f"Request failed: {str(e)}") from e

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a GET request."""
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a POST request."""
        return self._request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a PUT request."""
        return self._request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a DELETE request."""
        return self._request('DELETE', endpoint, **kwargs)

    def get_status(self) -> Dict[str, Any]:
        """Get the status of the Nexus server."""
        response = self.get('/v1/status')
        return response.json() if response.content else {}

    def is_writable(self) -> bool:
        """Check if the Nexus server is in read-only mode."""
        response = self.get('/v1/read-only')
        data = response.json() if response.content else {}
        return not data.get('frozen', True)

    def close(self):
        """Close the session and cleanup resources."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
