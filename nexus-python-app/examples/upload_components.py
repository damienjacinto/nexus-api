#!/usr/bin/env python3
"""
Example: Upload and manage components.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config
from nexus_client.exceptions import NexusException


def create_sample_file():
    """Create a sample file for upload demonstration."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write("Sample content for Nexus upload demo\n")
    temp_file.close()
    return temp_file.name


def main():
    """Demonstrate component upload and management."""

    config = Config()

    with NexusClient(**config.get_client_kwargs()) as client:

        print("=" * 60)
        print("Component Upload & Management Examples")
        print("=" * 60)

        # First, create a raw repository for testing
        repo_name = "raw-demo"
        print(f"\n1. Creating '{repo_name}' repository...")
        try:
            # Note: You'll need to implement create_raw_hosted in repositories.py
            # For now, assume it exists or use an existing repository
            print(f"   ℹ Using existing repository '{repo_name}'")
            print(f"   (Make sure this repository exists)")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Upload a raw component
        print("\n2. Uploading a raw component...")
        sample_file = create_sample_file()
        try:
            client.components.upload_raw(
                repository=repo_name,
                directory="demo/folder",
                filename="sample.txt",
                file_path=sample_file
            )
            print(f"   ✓ Uploaded file to {repo_name}/demo/folder/sample.txt")
        except NexusException as e:
            if e.status_code == 404:
                print(f"   ✗ Repository '{repo_name}' not found")
                print(f"   Please create the repository first")
            else:
                print(f"   ✗ Error: {e}")
        finally:
            # Clean up temp file
            os.unlink(sample_file)

        # List components in repository
        print("\n3. Listing components in repository...")
        try:
            result = client.components.list(repository=repo_name)
            items = result.get('items', [])
            print(f"   Found {len(items)} components")

            for item in items[:5]:
                print(f"\n   Component: {item['name']}")
                print(f"   Group: {item.get('group', 'N/A')}")
                print(f"   Version: {item.get('version', 'N/A')}")
                print(f"   Assets: {len(item.get('assets', []))}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Search for components
        print("\n4. Searching for uploaded component...")
        try:
            result = client.search.search(
                repository=repo_name,
                name="sample.txt"
            )
            items = result.get('items', [])

            if items:
                print(f"   ✓ Found component")
                component = items[0]
                component_id = component['id']
                print(f"   Component ID: {component_id}")

                # Get component details
                print("\n5. Getting component details...")
                details = client.components.get(component_id)
                print(f"   Name: {details['name']}")
                print(f"   Format: {details['format']}")
                print(f"   Repository: {details['repository']}")

                # List assets
                if 'assets' in details:
                    print(f"\n   Assets ({len(details['assets'])}):")
                    for asset in details['assets']:
                        print(f"   - {asset['path']}")
                        print(f"     Download: {asset['downloadUrl']}")
                        print(f"     Size: {asset.get('fileSize', 'unknown')} bytes")

                # Delete component (commented out to avoid accidental deletion)
                # print("\n6. Deleting component...")
                # client.components.delete(component_id)
                # print(f"   ✓ Component deleted")

            else:
                print(f"   ℹ Component not found")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Example: Upload Maven component (requires JAR file)
        print("\n7. Maven upload example (requires actual JAR file)...")
        print("   # Example code:")
        print("   client.components.upload_maven(")
        print("       repository='maven-releases',")
        print("       group_id='com.example',")
        print("       artifact_id='my-artifact',")
        print("       version='1.0.0',")
        print("       file_path='path/to/artifact.jar',")
        print("       packaging='jar'")
        print("   )")

        # Example: Upload NPM package
        print("\n8. NPM upload example (requires .tgz package)...")
        print("   # Example code:")
        print("   client.components.upload_npm(")
        print("       repository='npm-hosted',")
        print("       package_path='path/to/package-1.0.0.tgz'")
        print("   )")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
