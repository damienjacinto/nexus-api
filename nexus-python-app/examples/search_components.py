#!/usr/bin/env python3
"""
Example: Search for components in Nexus repositories.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config


def main():
    """Demonstrate component search functionality."""

    config = Config()

    with NexusClient(**config.get_client_kwargs()) as client:

        print("=" * 60)
        print("Component Search Examples")
        print("=" * 60)

        # Example 1: Search all components in a specific repository
        print("\n1. Searching for components in maven-central...")
        try:
            result = client.search.search(
                repository="maven-central",
                format="maven2"
            )

            items = result.get('items', [])
            print(f"   Found {len(items)} components")

            for item in items[:3]:  # Show first 3
                print(f"\n   Component: {item['group']}.{item['name']}")
                print(f"   Version: {item['version']}")
                print(f"   Repository: {item['repository']}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Example 2: Search by component name
        print("\n2. Searching for components by name...")
        try:
            result = client.search.search(
                name="junit",
                format="maven2"
            )

            items = result.get('items', [])
            print(f"   Found {len(items)} components matching 'junit'")

            for item in items[:3]:
                print(f"\n   {item['group']}.{item['name']}:{item['version']}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Example 3: Search by group and name
        print("\n3. Searching for specific group and artifact...")
        try:
            result = client.search.search(
                group="org.junit.jupiter",
                name="junit-jupiter-api"
            )

            items = result.get('items', [])
            print(f"   Found {len(items)} versions")

            for item in items[:5]:
                print(f"   - Version {item['version']}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Example 4: Search assets by checksum
        print("\n4. Searching assets by SHA-1 checksum...")
        print("   (You would need a real SHA-1 hash for this)")
        # try:
        #     result = client.search.search_assets(
        #         sha1="your-sha1-hash-here"
        #     )
        #     items = result.get('items', [])
        #     print(f"   Found {len(items)} matching assets")
        # except Exception as e:
        #     print(f"   ✗ Error: {e}")

        # Example 5: Pagination example
        print("\n5. Demonstrating pagination...")
        try:
            all_components = []
            continuation_token = None
            page = 1

            while page <= 3:  # Get first 3 pages
                result = client.search.search(
                    repository="maven-central",
                    continuation_token=continuation_token
                )

                items = result.get('items', [])
                all_components.extend(items)
                continuation_token = result.get('continuationToken')

                print(f"   Page {page}: {len(items)} components")

                if not continuation_token:
                    break

                page += 1

            print(f"   Total components retrieved: {len(all_components)}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
