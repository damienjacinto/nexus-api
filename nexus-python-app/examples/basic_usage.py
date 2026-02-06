#!/usr/bin/env python3
"""
Basic example demonstrating Nexus client usage.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config


def main():
    """Demonstrate basic Nexus client operations."""

    # Load configuration from .env file
    config = Config()

    # Or create client directly with credentials
    # client = NexusClient(
    #     base_url="https://nexus.example.com",
    #     username="admin",
    #     password="admin123"
    # )

    # Create client using config
    with NexusClient(**config.get_client_kwargs()) as client:

        print("=" * 60)
        print("Nexus Repository Manager - Python Client Demo")
        print("=" * 60)

        # Check server status
        print("\n1. Checking Nexus server status...")
        try:
            status = client.get_status()
            print(f"   ✓ Server is online")
            print(f"   Version: {status.get('Server', 'unknown')}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return

        # Check if server is writable
        print("\n2. Checking if server is writable...")
        try:
            is_writable = client.is_writable()
            print(f"   {'✓' if is_writable else '✗'} Server is {'writable' if is_writable else 'read-only'}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # List repositories
        print("\n3. Listing repositories...")
        try:
            repos = client.repositories.list()
            print(f"   Found {len(repos)} repositories:")
            for repo in repos[:5]:  # Show first 5
                print(f"   - {repo['name']} ({repo['format']}) - {repo['type']}")
            if len(repos) > 5:
                print(f"   ... and {len(repos) - 5} more")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # List blob stores
        print("\n4. Listing blob stores...")
        try:
            blob_stores = client.blob_stores.list()
            print(f"   Found {len(blob_stores)} blob stores:")
            for bs in blob_stores:
                print(f"   - {bs['name']} ({bs.get('type', 'unknown')})")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # List users (requires admin privileges)
        print("\n5. Listing users...")
        try:
            users = client.security.list_users()
            print(f"   Found {len(users)} users:")
            for user in users[:5]:  # Show first 5
                print(f"   - {user['userId']} ({user['firstName']} {user['lastName']})")
            if len(users) > 5:
                print(f"   ... and {len(users) - 5} more")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # List roles
        print("\n6. Listing roles...")
        try:
            roles = client.security.list_roles()
            print(f"   Found {len(roles)} roles:")
            for role in roles[:5]:  # Show first 5
                print(f"   - {role['id']}: {role['name']}")
            if len(roles) > 5:
                print(f"   ... and {len(roles) - 5} more")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # List tasks
        print("\n7. Listing scheduled tasks...")
        try:
            tasks = client.tasks.list()
            print(f"   Found {len(tasks)} tasks:")
            for task in tasks[:5]:  # Show first 5
                print(f"   - {task['name']} ({task['type']})")
            if len(tasks) > 5:
                print(f"   ... and {len(tasks) - 5} more")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        print("\n" + "=" * 60)
        print("Demo completed!")
        print("=" * 60)


if __name__ == "__main__":
    main()
