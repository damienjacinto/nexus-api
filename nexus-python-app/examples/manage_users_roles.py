#!/usr/bin/env python3
"""
Example: User and role management.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config
from nexus_client.exceptions import NexusException


def main():
    """Demonstrate user and role management."""

    config = Config()

    with NexusClient(**config.get_client_kwargs()) as client:

        print("=" * 60)
        print("User & Role Management Examples")
        print("=" * 60)

        # List existing users
        print("\n1. Listing existing users...")
        try:
            users = client.security.list_users()
            print(f"   Found {len(users)} users")

            for user in users[:5]:
                print(f"   - {user['userId']}: {user['firstName']} {user['lastName']}")
                print(f"     Email: {user['emailAddress']}")
                print(f"     Status: {user['status']}")
                print(f"     Roles: {', '.join(user.get('roles', []))}")
                print()

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # List roles
        print("\n2. Listing roles...")
        try:
            roles = client.security.list_roles()
            print(f"   Found {len(roles)} roles")

            for role in roles[:10]:
                print(f"   - {role['id']}: {role['name']}")
                if role.get('description'):
                    print(f"     {role['description']}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Create a new role
        print("\n3. Creating a new role...")
        role_id = "demo-developer"
        try:
            client.security.create_role(
                role_id=role_id,
                name="Demo Developer",
                description="Developer role for demonstration",
                privileges=["nx-repository-view-*-*-browse", "nx-repository-view-*-*-read"],
                roles=[]
            )
            print(f"   ✓ Created role '{role_id}'")
        except NexusException as e:
            if e.status_code == 400:
                print(f"   ℹ Role already exists or invalid configuration")
            else:
                print(f"   ✗ Error: {e}")

        # Create a new user
        print("\n4. Creating a new user...")
        user_id = "demo-user"
        try:
            user = client.security.create_user(
                user_id=user_id,
                first_name="Demo",
                last_name="User",
                email="demo@example.com",
                password="SecurePassword123!",
                roles=[role_id],
                status="active"
            )
            print(f"   ✓ Created user '{user_id}'")
            print(f"   User ID: {user['userId']}")
            print(f"   Email: {user['emailAddress']}")

        except NexusException as e:
            if e.status_code == 400:
                print(f"   ℹ User already exists or invalid configuration")
            else:
                print(f"   ✗ Error: {e}")

        # Update user
        print("\n5. Updating user...")
        try:
            client.security.update_user(
                user_id=user_id,
                first_name="Demo",
                last_name="User Updated",
                email="demo-updated@example.com",
                roles=[role_id, "nx-admin"],  # Add another role
                status="active"
            )
            print(f"   ✓ Updated user '{user_id}'")
        except NexusException as e:
            if e.status_code == 404:
                print(f"   ℹ User '{user_id}' not found")
            else:
                print(f"   ✗ Error: {e}")

        # Change password
        print("\n6. Changing user password...")
        try:
            client.security.change_password(
                user_id=user_id,
                new_password="NewSecurePassword456!"
            )
            print(f"   ✓ Changed password for user '{user_id}'")
        except NexusException as e:
            if e.status_code == 404:
                print(f"   ℹ User '{user_id}' not found")
            else:
                print(f"   ✗ Error: {e}")

        # List privileges
        print("\n7. Listing privileges (first 10)...")
        try:
            privileges = client.security.list_privileges()
            print(f"   Found {len(privileges)} privileges")

            for priv in privileges[:10]:
                print(f"   - {priv['name']}: {priv.get('type', 'unknown')}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Get specific role details
        print("\n8. Getting role details...")
        try:
            role = client.security.get_role(role_id)
            print(f"   Role: {role['name']}")
            print(f"   Description: {role.get('description', 'N/A')}")
            print(f"   Privileges: {', '.join(role.get('privileges', []))}")
            print(f"   Contained Roles: {', '.join(role.get('roles', []))}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Clean up - delete demo user and role
        print("\n9. Cleaning up demo user and role...")
        try:
            client.security.delete_user(user_id)
            print(f"   ✓ Deleted user '{user_id}'")
        except NexusException as e:
            if e.status_code == 404:
                print(f"   ℹ User '{user_id}' not found")
            else:
                print(f"   ✗ Error: {e}")

        try:
            client.security.delete_role(role_id)
            print(f"   ✓ Deleted role '{role_id}'")
        except NexusException as e:
            if e.status_code == 404:
                print(f"   ℹ Role '{role_id}' not found")
            else:
                print(f"   ✗ Error: {e}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
