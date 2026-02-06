"""Repository management API."""

from typing import List, Dict, Any, Optional


class RepositoryAPI:
    """API for managing Nexus repositories."""

    def __init__(self, client):
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all repositories.

        Returns:
            List of repository configurations
        """
        response = self.client.get('/v1/repositories')
        return response.json()

    def get(self, repository_name: str) -> Dict[str, Any]:
        """
        Get details of a specific repository.

        Args:
            repository_name: Name of the repository

        Returns:
            Repository configuration
        """
        response = self.client.get(f'/v1/repositories/{repository_name}')
        return response.json()

    def create_maven_hosted(
        self,
        name: str,
        blob_store: str = "default",
        strict_content_validation: bool = True,
        version_policy: str = "RELEASE",
        layout_policy: str = "STRICT",
        write_policy: str = "ALLOW"
    ) -> None:
        """
        Create a Maven hosted repository.

        Args:
            name: Repository name
            blob_store: Blob store to use
            strict_content_validation: Enable strict content type validation
            version_policy: Version policy (RELEASE, SNAPSHOT, MIXED)
            layout_policy: Layout policy (STRICT, PERMISSIVE)
            write_policy: Write policy (ALLOW, ALLOW_ONCE, DENY)
        """
        data = {
            "name": name,
            "online": True,
            "storage": {
                "blobStoreName": blob_store,
                "strictContentTypeValidation": strict_content_validation,
                "writePolicy": write_policy
            },
            "maven": {
                "versionPolicy": version_policy,
                "layoutPolicy": layout_policy
            }
        }
        self.client.post('/v1/repositories/maven/hosted', json=data)

    def create_docker_hosted(
        self,
        name: str,
        http_port: Optional[int] = None,
        https_port: Optional[int] = None,
        blob_store: str = "default",
        write_policy: str = "ALLOW"
    ) -> None:
        """
        Create a Docker hosted repository.

        Args:
            name: Repository name
            http_port: HTTP port for Docker registry
            https_port: HTTPS port for Docker registry
            blob_store: Blob store to use
            write_policy: Write policy (ALLOW, ALLOW_ONCE, DENY)
        """
        data = {
            "name": name,
            "online": True,
            "storage": {
                "blobStoreName": blob_store,
                "strictContentTypeValidation": True,
                "writePolicy": write_policy
            },
            "docker": {
                "v1Enabled": False,
                "forceBasicAuth": True
            }
        }

        if http_port:
            data["docker"]["httpPort"] = http_port
        if https_port:
            data["docker"]["httpsPort"] = https_port

        self.client.post('/v1/repositories/docker/hosted', json=data)

    def create_npm_hosted(
        self,
        name: str,
        blob_store: str = "default",
        write_policy: str = "ALLOW"
    ) -> None:
        """
        Create an NPM hosted repository.

        Args:
            name: Repository name
            blob_store: Blob store to use
            write_policy: Write policy (ALLOW, ALLOW_ONCE, DENY)
        """
        data = {
            "name": name,
            "online": True,
            "storage": {
                "blobStoreName": blob_store,
                "strictContentTypeValidation": True,
                "writePolicy": write_policy
            }
        }
        self.client.post('/v1/repositories/npm/hosted', json=data)

    def delete(self, repository_name: str) -> None:
        """
        Delete a repository.

        Args:
            repository_name: Name of the repository to delete
        """
        self.client.delete(f'/v1/repositories/{repository_name}')
