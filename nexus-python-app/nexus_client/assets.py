"""Assets management API."""

from typing import List, Dict, Any, Optional


class AssetAPI:
    """API for managing assets in Nexus repositories."""

    def __init__(self, client):
        self.client = client

    def list(
        self,
        repository: str,
        continuation_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List assets in a repository.

        Args:
            repository: Repository name
            continuation_token: Token for pagination

        Returns:
            Dict with 'items' (list of assets) and 'continuationToken'
        """
        params = {'repository': repository}
        if continuation_token:
            params['continuationToken'] = continuation_token

        response = self.client.get('/v1/assets', params=params)
        return response.json()

    def get(self, asset_id: str) -> Dict[str, Any]:
        """
        Get asset details by ID.

        Args:
            asset_id: Asset ID

        Returns:
            Asset details
        """
        response = self.client.get(f'/v1/assets/{asset_id}')
        return response.json()

    def delete(self, asset_id: str) -> None:
        """
        Delete an asset.

        Args:
            asset_id: Asset ID to delete
        """
        self.client.delete(f'/v1/assets/{asset_id}')

    def download(self, asset_id: str, output_path: str) -> None:
        """
        Download an asset to a file.

        Args:
            asset_id: Asset ID
            output_path: Path to save the downloaded file
        """
        asset = self.get(asset_id)
        download_url = asset.get('downloadUrl')

        if not download_url:
            raise ValueError(f"Asset {asset_id} has no download URL")

        response = self.client.session.get(
            download_url,
            verify=self.client.verify_ssl,
            timeout=self.client.timeout,
            stream=True
        )
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
