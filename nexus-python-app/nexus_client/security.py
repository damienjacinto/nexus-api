"""Security management API for users, roles, and privileges."""

from typing import List, Dict, Any, Optional


class SecurityAPI:
    """API for managing security (users, roles, privileges)."""

    def __init__(self, client):
        self.client = client

    # User Management
    def list_users(
        self,
        user_id: Optional[str] = None,
        source: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List users.

        Args:
            user_id: Optional user ID to filter by
            source: Optional user source to filter by

        Returns:
            List of users
        """
        params = {}
        if user_id:
            params['userId'] = user_id
        if source:
            params['source'] = source

        response = self.client.get('/v1/security/users', params=params)
        return response.json()

    def create_user(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        roles: List[str],
        status: str = "active"
    ) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            user_id: User ID
            first_name: First name
            last_name: Last name
            email: Email address
            password: Password
            roles: List of role IDs
            status: User status (active, disabled)

        Returns:
            Created user details
        """
        data = {
            "userId": user_id,
            "firstName": first_name,
            "lastName": last_name,
            "emailAddress": email,
            "password": password,
            "roles": roles,
            "status": status
        }

        response = self.client.post('/v1/security/users', json=data)
        return response.json()

    def update_user(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        roles: List[str],
        status: str = "active"
    ) -> None:
        """
        Update an existing user.

        Args:
            user_id: User ID
            first_name: First name
            last_name: Last name
            email: Email address
            roles: List of role IDs
            status: User status
        """
        data = {
            "userId": user_id,
            "firstName": first_name,
            "lastName": last_name,
            "emailAddress": email,
            "roles": roles,
            "status": status
        }

        self.client.put(f'/v1/security/users/{user_id}', json=data)

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user.

        Args:
            user_id: User ID to delete
        """
        self.client.delete(f'/v1/security/users/{user_id}')

    def change_password(self, user_id: str, new_password: str) -> None:
        """
        Change a user's password.

        Args:
            user_id: User ID
            new_password: New password
        """
        self.client.put(
            f'/v1/security/users/{user_id}/change-password',
            data=new_password,
            headers={'Content-Type': 'text/plain'}
        )

    # Role Management
    def list_roles(self, source: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List roles.

        Args:
            source: Optional source to filter by

        Returns:
            List of roles
        """
        params = {}
        if source:
            params['source'] = source

        response = self.client.get('/v1/security/roles', params=params)
        return response.json()

    def get_role(self, role_id: str, source: str = "default") -> Dict[str, Any]:
        """
        Get role details.

        Args:
            role_id: Role ID
            source: Role source

        Returns:
            Role details
        """
        response = self.client.get(f'/v1/security/roles/{source}/{role_id}')
        return response.json()

    def create_role(
        self,
        role_id: str,
        name: str,
        description: str = "",
        privileges: Optional[List[str]] = None,
        roles: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new role.

        Args:
            role_id: Role ID
            name: Role name
            description: Role description
            privileges: List of privilege IDs
            roles: List of contained role IDs

        Returns:
            Created role details
        """
        data = {
            "id": role_id,
            "name": name,
            "description": description,
            "privileges": privileges or [],
            "roles": roles or []
        }

        response = self.client.post('/v1/security/roles', json=data)
        return response.json()

    def update_role(
        self,
        role_id: str,
        name: str,
        description: str = "",
        privileges: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        source: str = "default"
    ) -> None:
        """
        Update an existing role.

        Args:
            role_id: Role ID
            name: Role name
            description: Role description
            privileges: List of privilege IDs
            roles: List of contained role IDs
            source: Role source
        """
        data = {
            "id": role_id,
            "name": name,
            "description": description,
            "privileges": privileges or [],
            "roles": roles or []
        }

        self.client.put(f'/v1/security/roles/{source}/{role_id}', json=data)

    def delete_role(self, role_id: str, source: str = "default") -> None:
        """
        Delete a role.

        Args:
            role_id: Role ID
            source: Role source
        """
        self.client.delete(f'/v1/security/roles/{source}/{role_id}')

    # Privilege Management
    def list_privileges(self) -> List[Dict[str, Any]]:
        """
        List all privileges.

        Returns:
            List of privileges
        """
        response = self.client.get('/v1/security/privileges')
        return response.json()

    def get_privilege(self, privilege_name: str) -> Dict[str, Any]:
        """
        Get privilege details.

        Args:
            privilege_name: Privilege name

        Returns:
            Privilege details
        """
        response = self.client.get(f'/v1/security/privileges/{privilege_name}')
        return response.json()

    def delete_privilege(self, privilege_name: str) -> None:
        """
        Delete a privilege.

        Args:
            privilege_name: Privilege name
        """
        self.client.delete(f'/v1/security/privileges/{privilege_name}')
