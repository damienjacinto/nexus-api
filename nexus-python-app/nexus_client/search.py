"""Search API for finding components and assets."""

from typing import List, Dict, Any, Optional


class SearchAPI:
    """API for searching components and assets."""

    def __init__(self, client):
        self.client = client

    def search(
        self,
        repository: Optional[str] = None,
        format: Optional[str] = None,
        group: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        md5: Optional[str] = None,
        sha1: Optional[str] = None,
        sha256: Optional[str] = None,
        sha512: Optional[str] = None,
        continuation_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for components.

        Args:
            repository: Repository name
            format: Repository format (maven2, npm, docker, etc.)
            group: Component group (e.g., Maven groupId)
            name: Component name
            version: Component version
            md5: MD5 checksum
            sha1: SHA-1 checksum
            sha256: SHA-256 checksum
            sha512: SHA-512 checksum
            continuation_token: Token for pagination

        Returns:
            Dict with 'items' (list of components) and 'continuationToken'
        """
        params = {}

        if repository:
            params['repository'] = repository
        if format:
            params['format'] = format
        if group:
            params['group'] = group
        if name:
            params['name'] = name
        if version:
            params['version'] = version
        if md5:
            params['md5'] = md5
        if sha1:
            params['sha1'] = sha1
        if sha256:
            params['sha256'] = sha256
        if sha512:
            params['sha512'] = sha512
        if continuation_token:
            params['continuationToken'] = continuation_token

        response = self.client.get('/v1/search', params=params)
        return response.json()

    def search_assets(
        self,
        repository: Optional[str] = None,
        format: Optional[str] = None,
        group: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        md5: Optional[str] = None,
        sha1: Optional[str] = None,
        sha256: Optional[str] = None,
        sha512: Optional[str] = None,
        continuation_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for assets.

        Args:
            repository: Repository name
            format: Repository format
            group: Component group
            name: Component name
            version: Component version
            md5: MD5 checksum
            sha1: SHA-1 checksum
            sha256: SHA-256 checksum
            sha512: SHA-512 checksum
            continuation_token: Token for pagination

        Returns:
            Dict with 'items' (list of assets) and 'continuationToken'
        """
        params = {}

        if repository:
            params['repository'] = repository
        if format:
            params['format'] = format
        if group:
            params['group'] = group
        if name:
            params['name'] = name
        if version:
            params['version'] = version
        if md5:
            params['md5'] = md5
        if sha1:
            params['sha1'] = sha1
        if sha256:
            params['sha256'] = sha256
        if sha512:
            params['sha512'] = sha512
        if continuation_token:
            params['continuationToken'] = continuation_token

        response = self.client.get('/v1/search/assets', params=params)
        return response.json()
