"""Blob store management API."""

from typing import List, Dict, Any, Optional


class BlobStoreAPI:
    """API for managing blob stores."""

    def __init__(self, client):
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all blob stores.

        Returns:
            List of blob stores
        """
        response = self.client.get('/v1/blobstores')
        return response.json()

    def get_file_blob_store(self, name: str) -> Dict[str, Any]:
        """
        Get file blob store configuration.

        Args:
            name: Blob store name

        Returns:
            Blob store configuration
        """
        response = self.client.get(f'/v1/blobstores/file/{name}')
        return response.json()

    def create_file_blob_store(
        self,
        name: str,
        path: Optional[str] = None,
        soft_quota_type: Optional[str] = None,
        soft_quota_limit: Optional[int] = None
    ) -> None:
        """
        Create a file blob store.

        Args:
            name: Blob store name
            path: Path on disk (optional, defaults to data directory)
            soft_quota_type: Quota type (spaceRemainingQuota, spaceUsedQuota)
            soft_quota_limit: Quota limit in MB
        """
        data = {
            "name": name,
        }

        if path:
            data["path"] = path

        if soft_quota_type and soft_quota_limit:
            data["softQuota"] = {
                "type": soft_quota_type,
                "limit": soft_quota_limit
            }

        self.client.post('/v1/blobstores/file', json=data)

    def update_file_blob_store(
        self,
        name: str,
        path: Optional[str] = None,
        soft_quota_type: Optional[str] = None,
        soft_quota_limit: Optional[int] = None
    ) -> None:
        """
        Update a file blob store.

        Args:
            name: Blob store name
            path: Path on disk
            soft_quota_type: Quota type
            soft_quota_limit: Quota limit in MB
        """
        data = {
            "name": name,
        }

        if path:
            data["path"] = path

        if soft_quota_type and soft_quota_limit:
            data["softQuota"] = {
                "type": soft_quota_type,
                "limit": soft_quota_limit
            }

        self.client.put(f'/v1/blobstores/file/{name}', json=data)

    def delete(self, name: str) -> None:
        """
        Delete a blob store.

        Args:
            name: Blob store name
        """
        self.client.delete(f'/v1/blobstores/{name}')

    def get_quota_status(self, name: str) -> Dict[str, Any]:
        """
        Get blob store quota status.

        Args:
            name: Blob store name

        Returns:
            Quota status information
        """
        response = self.client.get(f'/v1/blobstores/{name}/quota-status')
        return response.json()
