#!/usr/bin/env python3
"""
Example: Manage repositories - create, update, and delete.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config
from nexus_client.exceptions import NexusException


def main():
    """Demonstrate repository management."""

    config = Config()

    with NexusClient(**config.get_client_kwargs()) as client:

        print("=" * 60)
        print("Repository Management Examples")
        print("=" * 60)

        # List existing repositories
        print("\n1. Listing existing repositories...")
        try:
            repos = client.repositories.list()
            print(f"   Found {len(repos)} repositories")

            # Group by format
            by_format = {}
            for repo in repos:
                fmt = repo.get('format', 'unknown')
                by_format[fmt] = by_format.get(fmt, 0) + 1

            for fmt, count in by_format.items():
                print(f"   - {fmt}: {count}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Create a Maven hosted repository
        print("\n2. Creating a Maven hosted repository...")
        repo_name = "maven-demo-repo"
        try:
            client.repositories.create_maven_hosted(
                name=repo_name,
                blob_store="default",
                version_policy="RELEASE",
                write_policy="ALLOW"
            )
            print(f"   ✓ Created repository '{repo_name}'")
        except NexusException as e:
            if e.status_code == 400:
                print(f"   ℹ Repository already exists or invalid configuration")
            else:
                print(f"   ✗ Error: {e}")

        # Create an NPM hosted repository
        print("\n3. Creating an NPM hosted repository...")
        npm_repo_name = "npm-demo-repo"
        try:
            client.repositories.create_npm_hosted(
                name=npm_repo_name,
                blob_store="default",
                write_policy="ALLOW"
            )
            print(f"   ✓ Created repository '{npm_repo_name}'")
        except NexusException as e:
            if e.status_code == 400:
                print(f"   ℹ Repository already exists or invalid configuration")
            else:
                print(f"   ✗ Error: {e}")

        # Create a Docker hosted repository
        print("\n4. Creating a Docker hosted repository...")
        docker_repo_name = "docker-demo-repo"
        try:
            client.repositories.create_docker_hosted(
                name=docker_repo_name,
                http_port=8082,
                blob_store="default",
                write_policy="ALLOW"
            )
            print(f"   ✓ Created repository '{docker_repo_name}'")
        except NexusException as e:
            if e.status_code == 400:
                print(f"   ℹ Repository already exists or invalid configuration")
            else:
                print(f"   ✗ Error: {e}")

        # Get repository details
        print("\n5. Getting repository details...")
        try:
            repo = client.repositories.get(repo_name)
            print(f"   Repository: {repo['name']}")
            print(f"   Format: {repo['format']}")
            print(f"   Type: {repo['type']}")
            print(f"   URL: {repo.get('url', 'N/A')}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Clean up - delete demo repositories
        print("\n6. Cleaning up demo repositories...")
        for demo_repo in [repo_name, npm_repo_name, docker_repo_name]:
            try:
                client.repositories.delete(demo_repo)
                print(f"   ✓ Deleted repository '{demo_repo}'")
            except NexusException as e:
                if e.status_code == 404:
                    print(f"   ℹ Repository '{demo_repo}' not found")
                else:
                    print(f"   ✗ Error deleting '{demo_repo}': {e}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
