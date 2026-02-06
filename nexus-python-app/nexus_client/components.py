"""Components management API."""

from typing import List, Dict, Any, Optional


class ComponentAPI:
    """API for managing components in Nexus repositories."""

    def __init__(self, client):
        self.client = client

    def list(
        self,
        repository: str,
        continuation_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List components in a repository.

        Args:
            repository: Repository name
            continuation_token: Token for pagination

        Returns:
            Dict with 'items' (list of components) and 'continuationToken'
        """
        params = {'repository': repository}
        if continuation_token:
            params['continuationToken'] = continuation_token

        response = self.client.get('/v1/components', params=params)
        return response.json()

    def get(self, component_id: str) -> Dict[str, Any]:
        """
        Get component details by ID.

        Args:
            component_id: Component ID

        Returns:
            Component details
        """
        response = self.client.get(f'/v1/components/{component_id}')
        return response.json()

    def delete(self, component_id: str) -> None:
        """
        Delete a component.

        Args:
            component_id: Component ID to delete
        """
        self.client.delete(f'/v1/components/{component_id}')

    def upload_maven(
        self,
        repository: str,
        group_id: str,
        artifact_id: str,
        version: str,
        file_path: str,
        packaging: str = "jar",
        generate_pom: bool = False
    ) -> None:
        """
        Upload a Maven component.

        Args:
            repository: Repository name
            group_id: Maven groupId
            artifact_id: Maven artifactId
            version: Version
            file_path: Path to file to upload
            packaging: Packaging type (jar, war, pom, etc.)
            generate_pom: Auto-generate POM file
        """
        with open(file_path, 'rb') as f:
            files = {
                'maven2.asset1': f,
            }
            data = {
                'maven2.groupId': group_id,
                'maven2.artifactId': artifact_id,
                'maven2.version': version,
                'maven2.asset1.extension': packaging,
                'maven2.generate-pom': str(generate_pom).lower()
            }

            self.client.post(
                f'/v1/components',
                params={'repository': repository},
                files=files,
                data=data
            )

    def upload_npm(
        self,
        repository: str,
        package_path: str
    ) -> None:
        """
        Upload an NPM package.

        Args:
            repository: Repository name
            package_path: Path to .tgz package file
        """
        with open(package_path, 'rb') as f:
            files = {
                'npm.asset': f,
            }

            self.client.post(
                f'/v1/components',
                params={'repository': repository},
                files=files
            )

    def upload_raw(
        self,
        repository: str,
        directory: str,
        filename: str,
        file_path: str
    ) -> None:
        """
        Upload a raw component.

        Args:
            repository: Repository name
            directory: Directory path in repository
            filename: Filename in repository
            file_path: Local file path
        """
        with open(file_path, 'rb') as f:
            files = {
                'raw.asset1': f,
            }
            data = {
                'raw.directory': directory,
                'raw.asset1.filename': filename,
            }

            self.client.post(
                f'/v1/components',
                params={'repository': repository},
                files=files,
                data=data
            )
